-- ============================================================================
-- Borrowing
-- ============================================================================

-- borrowings
CREATE TABLE IF NOT EXISTS borrowings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES student_profiles(id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES books(id) ON DELETE RESTRICT,
    borrowed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    due_at TIMESTAMPTZ,
    returned_at TIMESTAMPTZ,
    status VARCHAR(50) NOT NULL CHECK (status IN ('borrowed', 'returned', 'overdue', 'lost')),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
