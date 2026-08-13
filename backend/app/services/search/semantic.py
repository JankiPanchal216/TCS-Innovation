import json
import logging
from typing import List, Dict, Any, Optional
import time

from app.db.session import create_pool
from app.services.embeddings.ollama import OllamaEmbeddingProvider

logger = logging.getLogger(__name__)

class SemanticSearchService:
    def __init__(self):
        self.provider = OllamaEmbeddingProvider()
        
    async def search_books_by_embedding(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        
        start_time = time.time()
        
        # 1. Generate query embedding
        query_embedding = await self.provider.generate_embedding(query)
        embedding_latency_ms = (time.time() - start_time) * 1000
        
        model_name = self.provider.get_model_name()
        
        db_start_time = time.time()
        
        pool = await create_pool()
        
        results = []
        async with pool.acquire() as conn:
            # We first verify if there are any vectors with this model
            # This implicitly validates if the query model matches the catalog model
            model_exists = await conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM books WHERE embedding_model = $1 AND embedding IS NOT NULL)",
                model_name
            )
            
            if not model_exists:
                raise ValueError(f"No embeddings found for model '{model_name}'. Please generate embeddings first.")
                
            # Base query
            query_vector_str = f"[{','.join(map(str, query_embedding))}]"
            
            sql = """
                SELECT 
                    b.id as book_id,
                    b.title,
                    b.authors,
                    b.description,
                    b.categories,
                    b.thumbnail_url as thumbnail,
                    b.difficulty,
                    b.is_active as availability,
                    1 - (b.embedding <=> $1::vector) AS similarity
                FROM (
                    SELECT 
                        books.*,
                        (
                            SELECT array_agg(a.name) 
                            FROM book_authors ba 
                            JOIN authors a ON ba.author_id = a.id 
                            WHERE ba.book_id = books.id
                        ) as authors,
                        (
                            SELECT array_agg(c.name) 
                            FROM book_categories bc 
                            JOIN categories c ON bc.category_id = c.id 
                            WHERE bc.book_id = books.id
                        ) as categories
                    FROM books
                ) b
                WHERE b.embedding IS NOT NULL
                AND b.embedding_model = $2
            """
            
            params = [query_vector_str, model_name]
            param_idx = 3
            
            if filters:
                if 'difficulty' in filters and filters['difficulty']:
                    sql += f" AND b.difficulty = ${param_idx}"
                    params.append(filters['difficulty'])
                    param_idx += 1
                    
                if 'available_only' in filters and filters['available_only']:
                    sql += f" AND b.is_active = true"
                    
                # Note: other filters like category/department could be added here
                # checking against the arrays
            
            sql += f" ORDER BY b.embedding <=> $1::vector"
            sql += f" LIMIT ${param_idx}"
            params.append(limit)
            
            records = await conn.fetch(sql, *params)
            
            for r in records:
                results.append({
                    "book_id": str(r["book_id"]),
                    "title": r["title"],
                    "authors": r["authors"] or [],
                    "description": r["description"],
                    "categories": r["categories"] or [],
                    "thumbnail": r["thumbnail"],
                    "difficulty": r["difficulty"],
                    "available_copies": 1 if r["availability"] else 0, # Simplify availability mapping
                    "similarity": round(float(r["similarity"]), 4)
                })
                
        database_search_latency_ms = (time.time() - db_start_time) * 1000
        total_latency_ms = (time.time() - start_time) * 1000
        
        logger.info(f"Semantic search completed in {total_latency_ms:.2f}ms. Embedded in {embedding_latency_ms:.2f}ms, DB in {database_search_latency_ms:.2f}ms.")
        
        return {
            "query": query,
            "model": model_name,
            "results": results,
            "metrics": {
                "embedding_latency_ms": round(embedding_latency_ms, 2),
                "database_search_latency_ms": round(database_search_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2)
            }
        }
