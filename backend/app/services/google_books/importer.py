import argparse
import asyncio
import time
from typing import Dict, Any, List

from app.db.session import create_pool, close_pool
from app.services.google_books.client import GoogleBooksClient
from app.services.google_books.mapper import map_volume_to_book

# 10 core computer science subjects
UNIVERSITY_CSE_PRESET = [
    "Computer Science",
    "Artificial Intelligence",
    "Machine Learning",
    "Cybersecurity",
    "Computer Networks",
    "Operating Systems",
    "Database Management",
    "Software Engineering",
    "Cloud Computing",
    "Data Science"
]

class GoogleBooksImporter:
    def __init__(self, pool):
        self.pool = pool
        self.client = GoogleBooksClient()
        self.stats = {
            "requested": 0,
            "fetched": 0,
            "inserted": 0,
            "updated": 0,
            "skipped": 0,
            "authors_created": 0,
            "categories_created": 0,
            "relationships_created": 0,
            "errors": 0
        }

    async def upsert_author(self, conn, name: str) -> str:
        """Upsert author and return UUID."""
        # Find existing
        row = await conn.fetchrow("SELECT id FROM authors WHERE name = $1", name)
        if row:
            return str(row['id'])
        
        # Insert new
        try:
            author_id = await conn.fetchval(
                "INSERT INTO authors (name) VALUES ($1) RETURNING id",
                name
            )
            self.stats["authors_created"] += 1
            return str(author_id)
        except Exception as e:
            print(f"Error inserting author {name}: {e}")
            raise

    async def upsert_category(self, conn, name: str) -> str:
        """Upsert category and return UUID."""
        row = await conn.fetchrow("SELECT id FROM categories WHERE name = $1", name)
        if row:
            return str(row['id'])
            
        try:
            cat_id = await conn.fetchval(
                "INSERT INTO categories (name) VALUES ($1) RETURNING id",
                name
            )
            self.stats["categories_created"] += 1
            return str(cat_id)
        except Exception as e:
            print(f"Error inserting category {name}: {e}")
            raise

    async def link_book_author(self, conn, book_id: str, author_id: str):
        """Create book_authors relationship safely."""
        await conn.execute(
            """
            INSERT INTO book_authors (book_id, author_id)
            VALUES ($1, $2)
            ON CONFLICT (book_id, author_id) DO NOTHING
            """,
            book_id, author_id
        )
        # We won't tightly track relationships_created purely to avoid extra SELECT queries, 
        # but we can increment it safely as an estimate
        self.stats["relationships_created"] += 1

    async def link_book_category(self, conn, book_id: str, category_id: str):
        """Create book_categories relationship safely."""
        await conn.execute(
            """
            INSERT INTO book_categories (book_id, category_id)
            VALUES ($1, $2)
            ON CONFLICT (book_id, category_id) DO NOTHING
            """,
            book_id, category_id
        )
        self.stats["relationships_created"] += 1

    async def import_book(self, book_data: Dict[str, Any], dry_run: bool = False):
        """Process a single book map via transaction."""
        google_book_id = book_data["google_book_id"]
        
        if dry_run:
            self.stats["inserted"] += 1
            return

        async with self.pool.acquire() as conn:
            # Use a transaction for safe processing
            async with conn.transaction():
                try:
                    # 1. Upsert authors
                    author_ids = []
                    for author_name in book_data["_extracted_authors"]:
                        aid = await self.upsert_author(conn, author_name)
                        if aid: author_ids.append(aid)

                    # 2. Upsert categories
                    category_ids = []
                    for cat_name in book_data["_extracted_categories"]:
                        cid = await self.upsert_category(conn, cat_name)
                        if cid: category_ids.append(cid)

                    # 3. Check if book exists
                    existing_book = await conn.fetchrow(
                        "SELECT id FROM books WHERE google_book_id = $1", 
                        google_book_id
                    )
                    
                    if existing_book:
                        book_id = str(existing_book["id"])
                        # Update metadata
                        await conn.execute(
                            """
                            UPDATE books 
                            SET title = $1, subtitle = $2, description = $3, 
                                publisher = $4, published_date = $5, language = $6, 
                                page_count = $7, thumbnail_url = $8, preview_url = $9, 
                                difficulty = $10, subjects = $11, keywords = $12,
                                updated_at = NOW()
                            WHERE id = $13
                            """,
                            book_data["title"], book_data["subtitle"], book_data["description"],
                            book_data["publisher"], book_data["published_date"], book_data["language"],
                            book_data["page_count"], book_data["thumbnail_url"], book_data["preview_url"],
                            book_data["difficulty"], book_data["subjects"], book_data["keywords"],
                            book_id
                        )
                        self.stats["updated"] += 1
                    else:
                        # Insert new book
                        book_id = await conn.fetchval(
                            """
                            INSERT INTO books (
                                google_book_id, isbn10, isbn13, title, subtitle, description, 
                                publisher, published_date, language, page_count, thumbnail_url, 
                                preview_url, difficulty, subjects, keywords
                            ) VALUES (
                                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15
                            ) RETURNING id
                            """,
                            google_book_id, book_data["isbn10"], book_data["isbn13"], book_data["title"], 
                            book_data["subtitle"], book_data["description"], book_data["publisher"], 
                            book_data["published_date"], book_data["language"], book_data["page_count"], 
                            book_data["thumbnail_url"], book_data["preview_url"], book_data["difficulty"], 
                            book_data["subjects"], book_data["keywords"]
                        )
                        self.stats["inserted"] += 1
                        book_id = str(book_id)

                    # 4. Link relationships
                    for aid in author_ids:
                        await self.link_book_author(conn, book_id, aid)
                        
                    for cid in category_ids:
                        await self.link_book_category(conn, book_id, cid)

                except Exception as e:
                    print(f"Error processing book {google_book_id}: {e}")
                    self.stats["errors"] += 1
                    raise # This rolls back the transaction

    async def run_query(self, query: str, limit: int, dry_run: bool = False):
        """Run a single query import."""
        self.stats["requested"] += limit
        print(f"Fetching '{query}' (limit {limit})...")
        
        raw_volumes = await self.client.search_books(query, max_results=limit)
        self.stats["fetched"] += len(raw_volumes)
        
        for raw in raw_volumes:
            mapped = map_volume_to_book(raw)
            if not mapped:
                self.stats["skipped"] += 1
                continue
                
            try:
                await self.import_book(mapped, dry_run)
            except Exception:
                # Already logged in import_book, just continue to next volume
                pass

    def print_summary(self, elapsed: float):
        print("\n==================================================")
        print("Google Books ingestion complete.")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        print("==================================================")
        print(f"Requested:             {self.stats['requested']}")
        print(f"Fetched:               {self.stats['fetched']}")
        print(f"Inserted:              {self.stats['inserted']}")
        print(f"Updated:               {self.stats['updated']}")
        print(f"Skipped:               {self.stats['skipped']}")
        print(f"Authors created:       {self.stats['authors_created']}")
        print(f"Categories created:    {self.stats['categories_created']}")
        print(f"Relationships created: {self.stats['relationships_created']}")
        print(f"Errors:                {self.stats['errors']}")
        print("==================================================\n")

async def async_main(args):
    pool = await create_pool()
    importer = GoogleBooksImporter(pool)
    
    start_time = time.time()
    
    if args.preset == "university-cse":
        print("Running university-cse preset...")
        for subject in UNIVERSITY_CSE_PRESET:
            await importer.run_query(subject, limit=50, dry_run=args.dry_run)
    elif args.query:
        await importer.run_query(args.query, limit=args.limit, dry_run=args.dry_run)
    else:
        print("Please provide a --query or --preset.")
        
    elapsed = time.time() - start_time
    importer.print_summary(elapsed)
    
    await close_pool()

def main():
    parser = argparse.ArgumentParser(description="Import books from Google Books API")
    parser.add_argument("--query", type=str, help="Search query for Google Books")
    parser.add_argument("--limit", type=int, default=50, help="Maximum number of books to fetch")
    parser.add_argument("--preset", type=str, choices=["university-cse"], help="Run a predefined preset import")
    parser.add_argument("--dry-run", action="store_true", help="Fetch data but do not write to the database")
    
    args = parser.parse_args()
    asyncio.run(async_main(args))

if __name__ == "__main__":
    main()
