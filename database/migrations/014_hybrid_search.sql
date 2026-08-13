-- ============================================================================
-- Phase 2C: Hybrid Search Implementation
-- ============================================================================

-- 1. Add the search_vector column to books
ALTER TABLE books ADD COLUMN IF NOT EXISTS search_vector tsvector;

-- 2. Create function to generate the weighted tsvector
CREATE OR REPLACE FUNCTION update_book_search_vector() RETURNS trigger AS $$
DECLARE
    v_authors text;
    v_categories text;
    v_book_id uuid;
BEGIN
    -- Determine which book_id we are updating
    IF TG_TABLE_NAME = 'books' THEN
        v_book_id := NEW.id;
    ELSIF TG_TABLE_NAME = 'book_authors' THEN
        IF TG_OP = 'DELETE' THEN v_book_id := OLD.book_id; ELSE v_book_id := NEW.book_id; END IF;
    ELSIF TG_TABLE_NAME = 'book_categories' THEN
        IF TG_OP = 'DELETE' THEN v_book_id := OLD.book_id; ELSE v_book_id := NEW.book_id; END IF;
    END IF;

    -- Aggregate authors
    SELECT string_agg(a.name, ' ') INTO v_authors
    FROM book_authors ba
    JOIN authors a ON ba.author_id = a.id
    WHERE ba.book_id = v_book_id;

    -- Aggregate categories, subjects, keywords
    SELECT string_agg(c.name, ' ') INTO v_categories
    FROM book_categories bc
    JOIN categories c ON bc.category_id = c.id
    WHERE bc.book_id = v_book_id;

    -- Update the search_vector for the specific book
    UPDATE books b
    SET search_vector = (
        setweight(to_tsvector('english', coalesce(b.title, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(b.subtitle, '') || ' ' || coalesce(v_authors, '')), 'B') ||
        setweight(to_tsvector('english', coalesce(array_to_string(b.subjects, ' '), '') || ' ' || coalesce(array_to_string(b.keywords, ' '), '') || ' ' || coalesce(v_categories, '')), 'C') ||
        setweight(to_tsvector('english', coalesce(b.description, '')), 'D')
    )
    WHERE b.id = v_book_id;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- 3. Create triggers
-- Note: FOR EACH ROW triggers on books don't need to do a separate UPDATE, but since we rely on joins, 
-- AFTER triggers are safer to ensure relational data is visible, or we just do it AFTER INSERT OR UPDATE.
-- For books:
DROP TRIGGER IF EXISTS trg_books_search_vector ON books;
CREATE TRIGGER trg_books_search_vector
AFTER INSERT OR UPDATE OF title, subtitle, description, subjects, keywords
ON books
FOR EACH ROW
EXECUTE FUNCTION update_book_search_vector();

-- For book_authors:
DROP TRIGGER IF EXISTS trg_book_authors_search_vector ON book_authors;
CREATE TRIGGER trg_book_authors_search_vector
AFTER INSERT OR UPDATE OR DELETE
ON book_authors
FOR EACH ROW
EXECUTE FUNCTION update_book_search_vector();

-- For book_categories:
DROP TRIGGER IF EXISTS trg_book_categories_search_vector ON book_categories;
CREATE TRIGGER trg_book_categories_search_vector
AFTER INSERT OR UPDATE OR DELETE
ON book_categories
FOR EACH ROW
EXECUTE FUNCTION update_book_search_vector();


-- 4. Create GIN index for full-text search
CREATE INDEX IF NOT EXISTS books_search_vector_idx ON books USING GIN (search_vector);

-- 5. Backfill existing books
-- We can invoke the function for all books by doing a dummy update
UPDATE books SET updated_at = NOW();
