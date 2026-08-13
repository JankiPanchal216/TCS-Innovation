from typing import List, Dict, Any
from app.db.session import create_pool

class CandidateGenerator:
    async def get_candidates(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Fetches candidate books for a given user, excluding books they have 
        already borrowed, saved, or dismissed.
        Since the catalog is small (~500 books), we fetch all eligible active books.
        """
        pool = await create_pool()
        
        sql = """
            SELECT 
                b.id as book_id,
                b.title,
                (
                    SELECT array_agg(a.name) 
                    FROM book_authors ba 
                    JOIN authors a ON ba.author_id = a.id 
                    WHERE ba.book_id = b.id
                ) as authors,
                b.description,
                (
                    SELECT array_agg(c.name) 
                    FROM book_categories bc 
                    JOIN categories c ON bc.category_id = c.id 
                    WHERE bc.book_id = b.id
                ) as categories,
                b.subjects,
                b.thumbnail_url as thumbnail,
                b.difficulty,
                b.is_active as availability,
                COALESCE(i.available_copies, 0) as available_copies
            FROM books b
            LEFT JOIN inventory i ON b.id = i.book_id
            WHERE b.is_active = true
            AND b.id NOT IN (
                -- Exclude borrowed
                SELECT book_id FROM borrowings WHERE student_id = (
                    SELECT id FROM student_profiles WHERE user_id = $1
                )
                UNION
                -- Exclude saved
                SELECT book_id FROM saved_books WHERE user_id = $1
                UNION
                -- Exclude dismissed
                SELECT r.book_id 
                FROM recommendation_feedback rf
                JOIN recommendations r ON rf.recommendation_id = r.id
                WHERE rf.user_id = $1 AND rf.feedback_type = 'dismissed'
            )
        """
        
        async with pool.acquire() as conn:
            records = await conn.fetch(sql, user_id)
            
            results = []
            for r in records:
                results.append({
                    "book_id": str(r["book_id"]),
                    "title": r["title"],
                    "authors": r["authors"] or [],
                    "description": r["description"],
                    "categories": r["categories"] or [],
                    "subjects": r["subjects"] or [],
                    "thumbnail": r["thumbnail"],
                    "difficulty": r["difficulty"],
                    "available_copies": r["available_copies"]
                })
                
            return results
