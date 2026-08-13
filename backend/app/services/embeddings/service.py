import json
import logging
from typing import List, Dict, Any, Optional
import time

from app.db.session import create_pool
from .base import EmbeddingProvider
from .text_builder import build_embedding_text

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, provider: EmbeddingProvider, batch_size: int = 16):
        self.provider = provider
        self.batch_size = batch_size

    async def _get_books_needing_embeddings(self, conn, limit: int = None, force: bool = False) -> List[dict]:
        model_name = self.provider.get_model_name()
        
        query = """
            SELECT 
                b.id, 
                b.title, 
                b.subtitle, 
                b.description, 
                b.subjects,
                (
                    SELECT array_agg(a.name) 
                    FROM book_authors ba 
                    JOIN authors a ON ba.author_id = a.id 
                    WHERE ba.book_id = b.id
                ) as authors,
                (
                    SELECT array_agg(c.name) 
                    FROM book_categories bc 
                    JOIN categories c ON bc.category_id = c.id 
                    WHERE bc.book_id = b.id
                ) as categories
            FROM books b
            WHERE b.is_active = true
        """
        
        if not force:
            query += f" AND (b.embedding IS NULL OR b.embedding_model != '{model_name}' OR b.embedding_updated_at IS NULL)"
            
        if limit:
            query += f" LIMIT {limit}"
            
        records = await conn.fetch(query)
        return [dict(r) for r in records]

    async def process_embeddings(self, limit: int = None, force: bool = False) -> Dict[str, Any]:
        pool = await create_pool()
        model_name = self.provider.get_model_name()
        
        stats = {
            "model": model_name,
            "books_processed": 0,
            "successful_embeddings": 0,
            "failed_embeddings": 0,
            "elapsed_time": 0.0,
            "dimensions": None
        }
        
        start_time = time.time()
        
        async with pool.acquire() as conn:
            books = await self._get_books_needing_embeddings(conn, limit, force)
            if not books:
                stats["elapsed_time"] = time.time() - start_time
                return stats
                
            stats["books_processed"] = len(books)
            
            # Process in batches
            for i in range(0, len(books), self.batch_size):
                batch = books[i:i + self.batch_size]
                
                # Build texts
                texts = []
                for book in batch:
                    texts.append(build_embedding_text(book))
                    
                # Call Ollama
                try:
                    embeddings = await self.provider.generate_embeddings(texts)
                    dimension = self.provider.get_dimension()
                    stats["dimensions"] = dimension
                    
                    # Ensure index exists
                    await self._ensure_vector_index(conn, dimension)
                    
                    # Update database in transaction
                    async with conn.transaction():
                        for idx, book in enumerate(batch):
                            # Convert embedding array to string format expected by pgvector
                            vector_str = f"[{','.join(map(str, embeddings[idx]))}]"
                            
                            await conn.execute("""
                                UPDATE books 
                                SET 
                                    embedding = $1::vector,
                                    embedding_model = $2,
                                    embedding_dimensions = $3,
                                    embedding_updated_at = NOW()
                                WHERE id = $4
                            """, vector_str, model_name, dimension, book['id'])
                            
                            stats["successful_embeddings"] += 1
                            
                except Exception as e:
                    logger.error(f"Failed to process batch {i // self.batch_size + 1}: {e}")
                    stats["failed_embeddings"] += len(batch)
                    
        stats["elapsed_time"] = time.time() - start_time
        return stats

    async def _ensure_vector_index(self, conn, dimension: int):
        # Create an expression index cast to the specific dimension if it doesn't exist
        index_name = f"books_embedding_idx_{dimension}"
        
        # Check if index exists
        exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1
                FROM pg_indexes
                WHERE indexname = $1
            )
        """, index_name)
        
        if not exists:
            logger.info(f"Creating HNSW index {index_name} for dimension {dimension}")
            await conn.execute(f"""
                CREATE INDEX IF NOT EXISTS {index_name} 
                ON books 
                USING hnsw ((embedding::vector({dimension})) vector_cosine_ops);
            """)

    async def get_status(self) -> Dict[str, Any]:
        pool = await create_pool()
        model_name = self.provider.get_model_name()
        
        async with pool.acquire() as conn:
            total_books = await conn.fetchval("SELECT COUNT(*) FROM books WHERE is_active = true")
            
            embedded_books = await conn.fetchval(f"""
                SELECT COUNT(*) FROM books 
                WHERE is_active = true 
                AND embedding IS NOT NULL 
                AND embedding_model = '{model_name}'
            """)
            
            missing = await conn.fetchval("""
                SELECT COUNT(*) FROM books 
                WHERE is_active = true 
                AND embedding IS NULL
            """)
            
            stale = await conn.fetchval(f"""
                SELECT COUNT(*) FROM books 
                WHERE is_active = true 
                AND embedding IS NOT NULL 
                AND embedding_model != '{model_name}'
            """)
            
            dim_row = await conn.fetchrow("""
                SELECT embedding_dimensions, embedding_updated_at 
                FROM books 
                WHERE is_active = true 
                AND embedding IS NOT NULL 
                AND embedding_model = $1
                ORDER BY embedding_updated_at DESC LIMIT 1
            """, model_name)
            
            dim = dim_row['embedding_dimensions'] if dim_row else None
            last_updated = dim_row['embedding_updated_at'] if dim_row else None
            
            return {
                "total_books": total_books or 0,
                "embedded": embedded_books or 0,
                "missing": missing or 0,
                "stale": stale or 0,
                "model": model_name,
                "dimensions": dim,
                "last_updated": str(last_updated) if last_updated else None,
                "failed": 0  # To track actual failures, we'd need a status column. This is a simplification.
            }
