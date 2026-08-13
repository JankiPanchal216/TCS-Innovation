import time
import logging
from typing import List, Dict, Any, Optional

from app.db.session import create_pool
from app.services.search.query import normalize_query

logger = logging.getLogger(__name__)

class KeywordSearchService:
    async def search_books_keyword(
        self,
        query: str,
        limit: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        
        start_time = time.time()
        normalized_query = normalize_query(query)
        
        pool = await create_pool()
        results = []
        
        async with pool.acquire() as conn:
            # We use websearch_to_tsquery which naturally handles plain text and logical operators
            
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
                    b.thumbnail_url as thumbnail,
                    b.difficulty,
                    COALESCE((SELECT SUM(available_copies) FROM inventory WHERE book_id = b.id), 0) as available_copies,
                    ts_rank_cd(b.search_vector, websearch_to_tsquery('english', $1)) AS keyword_score
                FROM books b
                WHERE b.search_vector @@ websearch_to_tsquery('english', $1)
            """
            
            params = [normalized_query]
            param_idx = 2
            
            if filters:
                if 'difficulty' in filters and filters['difficulty']:
                    sql += f" AND b.difficulty = ${param_idx}"
                    params.append(filters['difficulty'])
                    param_idx += 1
                    
                if 'available_only' in filters and filters['available_only']:
                    sql += f" AND (SELECT SUM(available_copies) FROM inventory WHERE book_id = b.id) > 0"
                    
            sql += f" ORDER BY keyword_score DESC"
            sql += f" LIMIT ${param_idx}"
            params.append(limit)
            
            records = await conn.fetch(sql, *params)
            
            for idx, r in enumerate(records):
                results.append({
                    "book_id": str(r["book_id"]),
                    "title": r["title"],
                    "authors": r["authors"] or [],
                    "description": r["description"],
                    "categories": r["categories"] or [],
                    "thumbnail": r["thumbnail"],
                    "difficulty": r["difficulty"],
                    "available_copies": r["available_copies"],
                    "keyword_score": round(float(r["keyword_score"]), 4),
                    "rank": idx + 1
                })
                
        database_search_latency_ms = (time.time() - start_time) * 1000
        
        logger.info(f"Keyword search completed in {database_search_latency_ms:.2f}ms. Query: '{normalized_query}'")
        
        return {
            "query": query,
            "normalized_query": normalized_query,
            "search_type": "keyword",
            "results": results,
            "metrics": {
                "keyword_latency_ms": round(database_search_latency_ms, 2),
                "total_latency_ms": round(database_search_latency_ms, 2)
            }
        }
