-- ============================================================================
-- Phase 2D: Inventory and Context Extensions
-- ============================================================================

-- 1. Modify Inventory Table
ALTER TABLE inventory 
ADD COLUMN IF NOT EXISTS inventory_source VARCHAR(50) DEFAULT 'manual' CHECK (inventory_source IN ('manual', 'csv', 'api', 'system')),
ADD COLUMN IF NOT EXISTS import_batch_id UUID,
ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'missing', 'retired')),
ADD COLUMN IF NOT EXISTS last_inventory_update TIMESTAMPTZ DEFAULT NOW();

-- 2. Inventory Import Batches
CREATE TABLE IF NOT EXISTS inventory_import_batches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    uploaded_by UUID REFERENCES users(id) ON DELETE SET NULL,
    filename VARCHAR(255) NOT NULL,
    total_rows INTEGER DEFAULT 0,
    successful_rows INTEGER DEFAULT 0,
    failed_rows INTEGER DEFAULT 0,
    duplicate_rows INTEGER DEFAULT 0,
    unresolved_rows INTEGER DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'uploaded' CHECK (status IN ('uploaded', 'validating', 'processing', 'completed', 'completed_with_errors', 'failed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- Foreign key for inventory to point back to the batch
ALTER TABLE inventory 
ADD CONSTRAINT fk_inventory_import_batch 
FOREIGN KEY (import_batch_id) REFERENCES inventory_import_batches(id) ON DELETE SET NULL;

-- 3. Inventory Import Errors
CREATE TABLE IF NOT EXISTS inventory_import_errors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    import_batch_id UUID NOT NULL REFERENCES inventory_import_batches(id) ON DELETE CASCADE,
    row_number INTEGER,
    error_type VARCHAR(100),
    error_message TEXT,
    raw_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Modify Student Profiles for Context
ALTER TABLE student_profiles
ADD COLUMN IF NOT EXISTS preferred_difficulty VARCHAR(50),
ADD COLUMN IF NOT EXISTS reading_goals TEXT[],
ADD COLUMN IF NOT EXISTS preferred_language VARCHAR(50) DEFAULT 'English',
ADD COLUMN IF NOT EXISTS preferred_book_type VARCHAR(50),
ADD COLUMN IF NOT EXISTS max_publication_age INTEGER,
ADD COLUMN IF NOT EXISTS availability_preference VARCHAR(50) DEFAULT 'any' CHECK (availability_preference IN ('any', 'available_only', 'physical_only', 'digital_only'));

-- 5. Extend Search Queries Analytics
ALTER TABLE search_queries
ADD COLUMN IF NOT EXISTS normalized_query TEXT,
ADD COLUMN IF NOT EXISTS parsed_intent JSONB,
ADD COLUMN IF NOT EXISTS personalization_enabled BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS available_results_count INTEGER,
ADD COLUMN IF NOT EXISTS top_result_id UUID REFERENCES books(id) ON DELETE SET NULL,
ADD COLUMN IF NOT EXISTS total_latency_ms INTEGER;

-- Trigger to keep last_inventory_update synced
CREATE OR REPLACE FUNCTION update_inventory_last_update()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_inventory_update = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trg_update_inventory_last_update
    BEFORE UPDATE ON inventory
    FOR EACH ROW
    EXECUTE FUNCTION update_inventory_last_update();
