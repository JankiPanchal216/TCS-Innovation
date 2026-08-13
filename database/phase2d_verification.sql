-- Phase 2D Verification Queries

-- 1. Check if tables exist
SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'inventory_import_batches');
SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'inventory_import_errors');

-- 2. Check inventory columns
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'inventory' AND column_name IN ('inventory_source', 'import_batch_id', 'status', 'last_inventory_update');

-- 3. Check student profile columns
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'student_profiles' AND column_name IN ('preferred_difficulty', 'reading_goals', 'availability_preference');

-- 4. Check query logs
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'search_queries' AND column_name IN ('parsed_intent', 'personalization_enabled', 'top_result_id');

-- 5. No orphan inventory rows
SELECT COUNT(*) FROM inventory WHERE book_id NOT IN (SELECT id FROM books);
