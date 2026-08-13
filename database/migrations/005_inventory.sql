-- ============================================================================
-- Inventory
-- ============================================================================

-- inventory
CREATE TABLE IF NOT EXISTS inventory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    total_copies INTEGER NOT NULL DEFAULT 0 CHECK (total_copies >= 0),
    available_copies INTEGER NOT NULL DEFAULT 0 CHECK (available_copies >= 0),
    location VARCHAR(255),
    shelf_code VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraint to ensure we don't have more available than total copies
    CONSTRAINT check_copies_validity CHECK (available_copies <= total_copies)
);

-- Triggers
CREATE TRIGGER update_inventory_modtime
    BEFORE UPDATE ON inventory
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
