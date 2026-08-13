-- ============================================================================
-- Catalog Entities
-- ============================================================================

-- authors
CREATE TABLE IF NOT EXISTS authors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    biography TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- books
CREATE TABLE IF NOT EXISTS books (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- External identity
    google_book_id VARCHAR(255) UNIQUE,
    isbn10 VARCHAR(10),
    isbn13 VARCHAR(13),
    
    -- Metadata
    title VARCHAR(255) NOT NULL,
    subtitle TEXT,
    description TEXT,
    publisher VARCHAR(255),
    published_date DATE,
    language VARCHAR(50),
    page_count INTEGER,
    thumbnail_url TEXT,
    preview_url TEXT,
    
    -- Classification
    difficulty VARCHAR(50),
    subjects TEXT[],
    keywords TEXT[],
    
    -- AI/search fields
    searchable_text TEXT,
    -- Using the generic vector type without dimension limit to be flexible for MVP
    embedding vector,
    embedding_model VARCHAR(100),
    embedding_dimensions INTEGER,
    embedding_updated_at TIMESTAMPTZ,
    
    -- Library fields
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- book_authors
CREATE TABLE IF NOT EXISTS book_authors (
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    author_id UUID REFERENCES authors(id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);

-- categories
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    parent_category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- book_categories
CREATE TABLE IF NOT EXISTS book_categories (
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, category_id)
);

-- course_books (Maps courses to relevant books)
CREATE TABLE IF NOT EXISTS course_books (
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    relevance_score NUMERIC(3, 2) CHECK (relevance_score >= 0 AND relevance_score <= 1),
    relevance_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (course_id, book_id)
);

-- Triggers
CREATE TRIGGER update_books_modtime
    BEFORE UPDATE ON books
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_course_books_modtime
    BEFORE UPDATE ON course_books
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
