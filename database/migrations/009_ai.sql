-- ============================================================================
-- AI Models and Learning Paths
-- ============================================================================

-- ai_models
CREATE TABLE IF NOT EXISTS ai_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider VARCHAR(100) NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    model_type VARCHAR(100) NOT NULL,
    is_local BOOLEAN NOT NULL DEFAULT true,
    is_active BOOLEAN NOT NULL DEFAULT true,
    capabilities JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ai_requests
CREATE TABLE IF NOT EXISTS ai_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    model_id UUID REFERENCES ai_models(id) ON DELETE SET NULL,
    request_type VARCHAR(100) NOT NULL CHECK (request_type IN ('intent_extraction', 'explanation', 'summarization', 'learning_path', 'research', 'chat')),
    input_tokens INTEGER,
    output_tokens INTEGER,
    latency_ms INTEGER,
    success BOOLEAN NOT NULL DEFAULT true,
    error_message TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- learning_paths
CREATE TABLE IF NOT EXISTS learning_paths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    goal TEXT,
    description TEXT,
    difficulty VARCHAR(50),
    estimated_hours NUMERIC(5, 2),
    generated_by_model UUID REFERENCES ai_models(id) ON DELETE SET NULL,
    model_version VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- learning_path_items
CREATE TABLE IF NOT EXISTS learning_path_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    learning_path_id UUID NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
    book_id UUID REFERENCES books(id) ON DELETE SET NULL,
    sequence_number INTEGER NOT NULL,
    rationale TEXT,
    estimated_hours NUMERIC(5, 2),
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed')),
    UNIQUE (learning_path_id, sequence_number)
);

-- Triggers
CREATE TRIGGER update_ai_models_modtime
    BEFORE UPDATE ON ai_models
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_learning_paths_modtime
    BEFORE UPDATE ON learning_paths
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
