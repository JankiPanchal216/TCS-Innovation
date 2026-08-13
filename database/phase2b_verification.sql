-- ============================================================================
-- Phase 2B Verification Script
-- ============================================================================

-- 1. Number of books
SELECT COUNT(*) as total_books FROM books;

-- 2. Number of books with embeddings
SELECT COUNT(*) as books_with_embeddings FROM books WHERE embedding IS NOT NULL;

-- 3. Number missing embeddings
SELECT COUNT(*) as missing_embeddings FROM books WHERE embedding IS NULL AND is_active = true;

-- 4. Number of embedding models
SELECT COUNT(DISTINCT embedding_model) as num_embedding_models FROM books WHERE embedding IS NOT NULL;

-- 5. Active embedding models
SELECT embedding_model, COUNT(*) as count 
FROM books 
WHERE embedding IS NOT NULL 
GROUP BY embedding_model;

-- 6. Embedding dimensions
SELECT DISTINCT embedding_dimensions as valid_dimensions FROM books WHERE embedding IS NOT NULL;

-- 7. Check for vectors with mismatched actual dimensions
SELECT id, title, vector_dims(embedding) as actual_dim, embedding_dimensions as recorded_dim
FROM books
WHERE embedding IS NOT NULL 
AND vector_dims(embedding) != embedding_dimensions;

-- 8. Check if vector HNSW index exists (for the hnsw index dynamically created)
SELECT 
    indexname, 
    indexdef 
FROM pg_indexes 
WHERE tablename = 'books' AND indexname LIKE 'books_embedding_idx_%';
