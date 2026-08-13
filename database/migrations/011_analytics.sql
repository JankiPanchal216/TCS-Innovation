-- ============================================================================
-- Analytics and Acquisition
-- ============================================================================

-- acquisition_recommendations
CREATE TABLE IF NOT EXISTS acquisition_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    recommendation_type VARCHAR(50) NOT NULL CHECK (recommendation_type IN ('acquire', 'increase_copies', 'monitor', 'retire')),
    priority VARCHAR(50) NOT NULL CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    demand_score NUMERIC(5, 4),
    current_inventory INTEGER,
    estimated_demand INTEGER,
    reason TEXT,
    external_research JSONB,
    generated_by_model UUID REFERENCES ai_models(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Analytics Views

-- 1. book_popularity
CREATE OR REPLACE VIEW view_book_popularity AS
SELECT 
    b.id AS book_id,
    b.title,
    COUNT(DISTINCT bw.id) AS total_borrows,
    COUNT(DISTINCT bi.id) AS total_interactions,
    AVG(bw.rating) AS avg_rating
FROM books b
LEFT JOIN borrowings bw ON b.id = bw.book_id
LEFT JOIN book_interactions bi ON b.id = bi.book_id
GROUP BY b.id, b.title;

-- 2. book_utilization
CREATE OR REPLACE VIEW view_book_utilization AS
SELECT 
    b.id AS book_id,
    b.title,
    i.total_copies,
    i.available_copies,
    (i.total_copies - i.available_copies) AS currently_borrowed,
    CASE 
        WHEN i.total_copies > 0 THEN 
            ROUND(((i.total_copies - i.available_copies)::NUMERIC / i.total_copies) * 100, 2)
        ELSE 0 
    END AS utilization_percentage
FROM books b
JOIN inventory i ON b.id = i.book_id;

-- 3. subject_demand
CREATE OR REPLACE VIEW view_subject_demand AS
SELECT 
    unnest(b.subjects) AS subject,
    COUNT(DISTINCT bw.id) AS borrow_count,
    COUNT(DISTINCT bi.id) AS interaction_count
FROM books b
LEFT JOIN borrowings bw ON b.id = bw.book_id
LEFT JOIN book_interactions bi ON b.id = bi.book_id
GROUP BY subject;

-- 4. student_borrowing_summary
CREATE OR REPLACE VIEW view_student_borrowing_summary AS
SELECT 
    sp.id AS student_id,
    sp.student_number,
    COUNT(bw.id) AS total_borrowed,
    SUM(CASE WHEN bw.status = 'overdue' THEN 1 ELSE 0 END) AS overdue_count
FROM student_profiles sp
LEFT JOIN borrowings bw ON sp.id = bw.student_id
GROUP BY sp.id, sp.student_number;

-- 5. overdue_summary
CREATE OR REPLACE VIEW view_overdue_summary AS
SELECT 
    bw.id AS borrowing_id,
    sp.student_number,
    b.title,
    bw.due_at,
    EXTRACT(DAY FROM (NOW() - bw.due_at)) AS days_overdue
FROM borrowings bw
JOIN student_profiles sp ON bw.student_id = sp.id
JOIN books b ON bw.book_id = b.id
WHERE bw.status = 'overdue';

-- 6. recommendation_performance
CREATE OR REPLACE VIEW view_recommendation_performance AS
SELECT 
    r.recommendation_engine_version,
    COUNT(rf.id) AS total_feedback,
    SUM(CASE WHEN rf.feedback_type IN ('useful', 'saved', 'borrowed') THEN 1 ELSE 0 END) AS positive_feedback,
    SUM(CASE WHEN rf.feedback_type IN ('not_useful', 'dismissed') THEN 1 ELSE 0 END) AS negative_feedback
FROM recommendations r
LEFT JOIN recommendation_feedback rf ON r.id = rf.recommendation_id
GROUP BY r.recommendation_engine_version;

-- 7. inventory_status
CREATE OR REPLACE VIEW view_inventory_status AS
SELECT 
    location,
    SUM(total_copies) AS library_total_copies,
    SUM(available_copies) AS library_available_copies
FROM inventory
GROUP BY location;

-- 8. monthly_borrowing_trends
CREATE OR REPLACE VIEW view_monthly_borrowing_trends AS
SELECT 
    DATE_TRUNC('month', borrowed_at) AS month,
    COUNT(id) AS total_borrows
FROM borrowings
GROUP BY DATE_TRUNC('month', borrowed_at)
ORDER BY month DESC;
