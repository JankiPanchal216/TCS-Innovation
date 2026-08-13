-- ============================================================================
-- Interactions and Search
-- ============================================================================

-- book_interactions
CREATE TABLE IF NOT EXISTS book_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    book_id UUID REFERENCES books(id) ON DELETE SET NULL,
    interaction_type VARCHAR(50) NOT NULL CHECK (interaction_type IN ('search', 'view', 'save', 'unsave', 'recommend', 'borrow', 'return', 'rate', 'click')),
    search_query TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- saved_books
CREATE TABLE IF NOT EXISTS saved_books (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, book_id)
);

-- search_queries
CREATE TABLE IF NOT EXISTS search_queries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    query TEXT NOT NULL,
    search_type VARCHAR(50) NOT NULL CHECK (search_type IN ('keyword', 'semantic', 'hybrid', 'natural_language')),
    filters JSONB,
    results_count INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
