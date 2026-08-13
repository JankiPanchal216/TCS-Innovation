-- ============================================================================
-- Recommendations
-- ============================================================================

-- recommendations
CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    
    -- Scoring
    final_score NUMERIC(5, 4),
    semantic_score NUMERIC(5, 4),
    academic_score NUMERIC(5, 4),
    interest_score NUMERIC(5, 4),
    history_score NUMERIC(5, 4),
    popularity_score NUMERIC(5, 4),
    
    -- Explanation
    explanation TEXT,
    
    -- Recommendation context
    query TEXT,
    context JSONB,
    
    -- Model tracking
    recommendation_engine_version VARCHAR(100),
    embedding_model VARCHAR(100),
    llm_model VARCHAR(100),
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- recommendation_feedback
CREATE TABLE IF NOT EXISTS recommendation_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recommendation_id UUID NOT NULL REFERENCES recommendations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    feedback_type VARCHAR(50) NOT NULL CHECK (feedback_type IN ('useful', 'not_useful', 'saved', 'borrowed', 'dismissed')),
    feedback_value INTEGER,
    comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
