-- ============================================================================
-- Indexes
-- ============================================================================

-- users
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- student_profiles
CREATE INDEX IF NOT EXISTS idx_student_profiles_student_number ON student_profiles(student_number);

-- books
CREATE INDEX IF NOT EXISTS idx_books_google_book_id ON books(google_book_id);
CREATE INDEX IF NOT EXISTS idx_books_isbn13 ON books(isbn13);
CREATE INDEX IF NOT EXISTS idx_books_title ON books USING gin (to_tsvector('english', title));
CREATE INDEX IF NOT EXISTS idx_books_difficulty ON books(difficulty);
CREATE INDEX IF NOT EXISTS idx_books_published_date ON books(published_date);

-- Note: We are deferring HNSW/IVFFlat index creation for `embedding` columns
-- until the exact dimension and size are finalized for production, 
-- but a placeholder comment is here for when ready:
-- CREATE INDEX idx_books_embedding ON books USING hnsw (embedding vector_l2_ops);

-- courses
CREATE INDEX IF NOT EXISTS idx_courses_course_code ON courses(course_code);

-- inventory
CREATE INDEX IF NOT EXISTS idx_inventory_available_copies ON inventory(available_copies);
CREATE INDEX IF NOT EXISTS idx_inventory_book_id ON inventory(book_id);

-- borrowings
CREATE INDEX IF NOT EXISTS idx_borrowings_student_id ON borrowings(student_id);
CREATE INDEX IF NOT EXISTS idx_borrowings_book_id ON borrowings(book_id);
CREATE INDEX IF NOT EXISTS idx_borrowings_status ON borrowings(status);
CREATE INDEX IF NOT EXISTS idx_borrowings_borrowed_at ON borrowings(borrowed_at);

-- book_interactions
CREATE INDEX IF NOT EXISTS idx_interactions_user_id ON book_interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_interactions_book_id ON book_interactions(book_id);

-- recommendations
CREATE INDEX IF NOT EXISTS idx_recommendations_user_id ON recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_book_id ON recommendations(book_id);

-- search_queries
CREATE INDEX IF NOT EXISTS idx_search_queries_user_id ON search_queries(user_id);

-- ai_requests
CREATE INDEX IF NOT EXISTS idx_ai_requests_user_id ON ai_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_requests_model_id ON ai_requests(model_id);
