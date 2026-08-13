-- ============================================================================
-- Example Queries for LibraAI
-- ============================================================================

-- 1. Keyword Book Search (using Full Text Search)
SELECT id, title, authors_list, difficulty 
FROM books b
LEFT JOIN LATERAL (
    SELECT string_agg(a.name, ', ') AS authors_list 
    FROM book_authors ba 
    JOIN authors a ON ba.author_id = a.id 
    WHERE ba.book_id = b.id
) a ON true
WHERE to_tsvector('english', b.title || ' ' || COALESCE(b.description, '')) @@ to_tsquery('english', 'database & management')
ORDER BY ts_rank(to_tsvector('english', b.title), to_tsquery('english', 'database & management')) DESC
LIMIT 10;

-- 2. Semantic Book Search (using pgvector)
-- Note: Replace '[0.1, 0.2, ...]' with an actual query embedding from your embedding model
SELECT id, title, description, difficulty, 
       1 - (embedding <=> '[0.1, 0.2, 0.3]') AS similarity_score
FROM books
WHERE embedding IS NOT NULL
ORDER BY embedding <=> '[0.1, 0.2, 0.3]'
LIMIT 10;

-- 3. Hybrid Search (Keyword + Semantic Filtering by Department)
SELECT b.id, b.title, b.difficulty, 
       1 - (b.embedding <=> '[0.1, 0.2, 0.3]') AS similarity_score
FROM books b
WHERE 'Computer Science' = ANY(b.subjects)
  AND b.difficulty = 'Advanced'
  AND b.embedding IS NOT NULL
ORDER BY b.embedding <=> '[0.1, 0.2, 0.3]'
LIMIT 10;

-- 4. Student's Borrowing History
SELECT b.title, bw.borrowed_at, bw.status, bw.returned_at, bw.rating
FROM borrowings bw
JOIN books b ON bw.book_id = b.id
JOIN student_profiles sp ON bw.student_id = sp.id
WHERE sp.student_number = 'STU2024000' -- Replace with actual student number
ORDER BY bw.borrowed_at DESC;

-- 5. Underutilized Books (Analytics View)
SELECT title, total_copies, available_copies, utilization_percentage
FROM view_book_utilization
WHERE utilization_percentage < 20.0 AND total_copies > 0
ORDER BY utilization_percentage ASC
LIMIT 10;

-- 6. Popular Books (Analytics View)
SELECT title, total_borrows, total_interactions, avg_rating
FROM view_book_popularity
ORDER BY total_borrows DESC, total_interactions DESC
LIMIT 10;

-- 7. Subject Demand (Analytics View)
SELECT subject, borrow_count, interaction_count
FROM view_subject_demand
ORDER BY interaction_count DESC
LIMIT 10;

-- 8. Acquisition Candidates
-- Find books in high-demand subjects with low available copies
SELECT b.title, b.subjects, i.total_copies, i.available_copies
FROM books b
JOIN inventory i ON b.id = i.book_id
WHERE b.subjects && ARRAY['Computer Science']
  AND i.total_copies > 0 
  AND (i.available_copies::float / i.total_copies) < 0.2
ORDER BY i.available_copies ASC;

-- 9. Insert a Recommendation (Demonstrating Scoring Formula support)
-- final_score = 0.30*semantic + 0.25*academic + 0.20*interest + 0.15*history + 0.10*popularity
/*
INSERT INTO recommendations (
    user_id, book_id, final_score, semantic_score, academic_score, 
    interest_score, history_score, popularity_score, explanation
) VALUES (
    'user-uuid-here', 'book-uuid-here', 0.85, 0.90, 0.80, 0.85, 0.70, 0.95,
    'This book is highly semantically similar to your query and aligns with your enrolled Data Structures course.'
);
*/
