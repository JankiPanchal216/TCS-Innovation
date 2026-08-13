-- ============================================================================
-- Phase 2C Verification Script
-- ============================================================================

-- 1. Check if the search_vector column was added
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'books' AND column_name = 'search_vector';

-- 2. Verify GIN index exists
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'books' AND indexname = 'books_search_vector_idx';

-- 3. Verify triggers are set up on books, book_authors, book_categories
SELECT trigger_name, event_object_table, event_manipulation, action_statement
FROM information_schema.triggers
WHERE trigger_name IN ('trg_books_search_vector', 'trg_book_authors_search_vector', 'trg_book_categories_search_vector');

-- 4. Check if search_vector is populated for existing books
SELECT count(*) as books_with_search_vector
FROM books 
WHERE search_vector IS NOT NULL;

-- 5. Test FTS manually (keyword: 'security')
SELECT id, title, ts_rank(search_vector, websearch_to_tsquery('english', 'security')) as rank 
FROM books 
WHERE search_vector @@ websearch_to_tsquery('english', 'security')
ORDER BY rank DESC 
LIMIT 5;

-- 6. View recent searches to verify search analytics logging
SELECT query, search_type, filters, results_count, created_at
FROM search_queries
ORDER BY created_at DESC
LIMIT 5;
