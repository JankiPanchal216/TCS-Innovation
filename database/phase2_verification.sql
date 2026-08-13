-- Phase 2 Verification Queries

-- 1. Verify books exist and count them
SELECT COUNT(*) AS total_books FROM books;

-- 2. Verify authors exist and count them
SELECT COUNT(*) AS total_authors FROM authors;

-- 3. Verify categories exist and count them
SELECT COUNT(*) AS total_categories FROM categories;

-- 4. Verify book_authors relationships
SELECT COUNT(*) AS total_book_authors FROM book_authors;
-- Check a sample to ensure mapping
SELECT b.title, a.name 
FROM books b 
JOIN book_authors ba ON b.id = ba.book_id 
JOIN authors a ON a.id = ba.author_id 
LIMIT 5;

-- 5. Verify book_categories relationships
SELECT COUNT(*) AS total_book_categories FROM book_categories;
-- Check a sample to ensure mapping
SELECT b.title, c.name 
FROM books b 
JOIN book_categories bc ON b.id = bc.book_id 
JOIN categories c ON c.id = bc.category_id 
LIMIT 5;

-- 6. Confirm no duplicate google_book_ids (should return 0)
SELECT google_book_id, COUNT(*) 
FROM books 
GROUP BY google_book_id 
HAVING COUNT(*) > 1;

-- 7. Confirm no orphan relationships
-- Should return 0
SELECT COUNT(*) FROM book_authors 
WHERE book_id NOT IN (SELECT id FROM books) 
   OR author_id NOT IN (SELECT id FROM authors);

-- Should return 0
SELECT COUNT(*) FROM book_categories 
WHERE book_id NOT IN (SELECT id FROM books) 
   OR category_id NOT IN (SELECT id FROM categories);
