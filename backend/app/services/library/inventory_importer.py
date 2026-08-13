import csv
import io
from typing import Dict, Any, List, Optional
import asyncpg
import json

class InventoryImporter:
    def __init__(self, pool):
        self.pool = pool

    def _normalize_isbn(self, isbn: str) -> Optional[str]:
        if not isbn:
            return None
        # Remove dashes and spaces
        clean = isbn.replace("-", "").replace(" ", "").strip()
        if len(clean) in (10, 13) and clean.isalnum():
            return clean
        return None

    def _normalize_string(self, val: str) -> str:
        if not val:
            return ""
        return " ".join(val.strip().split()).lower()

    async def _resolve_book_identity(self, conn: asyncpg.Connection, row: Dict[str, str]) -> Optional[str]:
        """Attempt to find an existing book by ISBN13, ISBN10, Google ID, or Title+Author."""
        
        # 1. Check ISBN13
        isbn13 = self._normalize_isbn(row.get("isbn13") or row.get("isbn_13") or row.get("isbn"))
        if isbn13 and len(isbn13) == 13:
            book_id = await conn.fetchval("SELECT id FROM books WHERE isbn13 = $1", isbn13)
            if book_id: return str(book_id)

        # 2. Check ISBN10
        isbn10 = self._normalize_isbn(row.get("isbn10") or row.get("isbn_10") or row.get("isbn"))
        if isbn10 and len(isbn10) == 10:
            book_id = await conn.fetchval("SELECT id FROM books WHERE isbn10 = $1", isbn10)
            if book_id: return str(book_id)

        # 3. Check Google Book ID
        google_id = row.get("google_book_id")
        if google_id:
            book_id = await conn.fetchval("SELECT id FROM books WHERE google_book_id = $1", google_id.strip())
            if book_id: return str(book_id)

        # 4. Check Title + Author (approximate)
        title = self._normalize_string(row.get("title") or row.get("book_title"))
        author = self._normalize_string(row.get("author") or row.get("authors"))
        
        if title and author:
            # We look for a book with an exact lower-case match on title, and an author that matches
            # This is complex in SQL due to the many-to-many relationship, so we do a simpler title match first
            records = await conn.fetch("SELECT id FROM books WHERE LOWER(title) = $1", title)
            for r in records:
                b_id = r["id"]
                # Check authors for this book
                authors = await conn.fetch(
                    "SELECT LOWER(name) as name FROM authors JOIN book_authors ON authors.id = book_authors.author_id WHERE book_id = $1", 
                    b_id
                )
                for a in authors:
                    if author in a["name"] or a["name"] in author:
                        return str(b_id)
        
        return None

    async def process_csv_upload(self, user_id: str, filename: str, content: bytes) -> Dict[str, Any]:
        stats = {
            "total_rows": 0,
            "successful_rows": 0,
            "failed_rows": 0,
            "duplicate_rows": 0,
            "books_created": 0,
            "inventory_updated": 0,
            "unresolved_rows": 0
        }

        # Parse CSV
        try:
            text = content.decode('utf-8-sig')
            reader = csv.DictReader(io.StringIO(text))
            rows = list(reader)
        except Exception as e:
            raise ValueError(f"Failed to parse CSV: {str(e)}")

        stats["total_rows"] = len(rows)
        
        if stats["total_rows"] == 0:
            return stats

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Create batch record
                batch_id = await conn.fetchval(
                    """
                    INSERT INTO inventory_import_batches (uploaded_by, filename, total_rows, status)
                    VALUES ($1, $2, $3, 'processing') RETURNING id
                    """,
                    user_id, filename, stats["total_rows"]
                )

                for idx, row in enumerate(rows, start=1):
                    # Clean headers/values
                    cleaned_row = {k.strip().lower(): v.strip() for k, v in row.items() if k and v}
                    
                    if not cleaned_row:
                        continue

                    # Require title and quantity at minimum
                    quantity_str = cleaned_row.get("quantity") or cleaned_row.get("copies") or cleaned_row.get("total_copies", "1")
                    try:
                        quantity = int(quantity_str)
                    except ValueError:
                        quantity = 1
                        
                    available_copies_str = cleaned_row.get("available_copies", str(quantity))
                    try:
                        available_copies = int(available_copies_str)
                    except ValueError:
                        available_copies = quantity

                    location = cleaned_row.get("location", "Main Library")
                    shelf = cleaned_row.get("shelf_code") or cleaned_row.get("shelf", None)

                    # Identity Resolution
                    book_id = await self._resolve_book_identity(conn, cleaned_row)

                    if not book_id:
                        # Mark unresolved
                        stats["unresolved_rows"] += 1
                        stats["failed_rows"] += 1
                        await conn.execute(
                            """
                            INSERT INTO inventory_import_errors (import_batch_id, row_number, error_type, error_message, raw_data)
                            VALUES ($1, $2, 'unresolved', 'Could not confidently match book to catalog', $3)
                            """,
                            batch_id, idx, json.dumps(cleaned_row)
                        )
                        continue

                    # Upsert Inventory
                    try:
                        # Check if inventory record exists for this book in this location
                        inv_id = await conn.fetchval(
                            "SELECT id FROM inventory WHERE book_id = $1 AND location = $2", 
                            book_id, location
                        )

                        if inv_id:
                            # Update existing
                            await conn.execute(
                                """
                                UPDATE inventory 
                                SET total_copies = $1, available_copies = $2, shelf_code = $3, 
                                    inventory_source = 'csv', import_batch_id = $4, updated_at = NOW()
                                WHERE id = $5
                                """,
                                quantity, available_copies, shelf, batch_id, inv_id
                            )
                            stats["inventory_updated"] += 1
                        else:
                            # Insert new
                            await conn.execute(
                                """
                                INSERT INTO inventory (book_id, total_copies, available_copies, location, shelf_code, inventory_source, import_batch_id)
                                VALUES ($1, $2, $3, $4, $5, 'csv', $6)
                                """,
                                book_id, quantity, available_copies, location, shelf, batch_id
                            )
                            stats["inventory_updated"] += 1
                            
                        stats["successful_rows"] += 1
                    except Exception as e:
                        stats["failed_rows"] += 1
                        await conn.execute(
                            """
                            INSERT INTO inventory_import_errors (import_batch_id, row_number, error_type, error_message, raw_data)
                            VALUES ($1, $2, 'upsert_error', $3, $4)
                            """,
                            batch_id, idx, str(e), json.dumps(cleaned_row)
                        )

                # Update batch status
                status = 'completed' if stats["failed_rows"] == 0 else 'completed_with_errors'
                if stats["successful_rows"] == 0 and stats["total_rows"] > 0:
                    status = 'failed'

                await conn.execute(
                    """
                    UPDATE inventory_import_batches 
                    SET successful_rows = $1, failed_rows = $2, duplicate_rows = $3, unresolved_rows = $4, 
                        status = $5, completed_at = NOW()
                    WHERE id = $6
                    """,
                    stats["successful_rows"], stats["failed_rows"], stats["duplicate_rows"], stats["unresolved_rows"], 
                    status, batch_id
                )

        return stats
