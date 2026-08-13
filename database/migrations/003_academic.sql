-- ============================================================================
-- Academic Entities
-- ============================================================================

-- departments
CREATE TABLE IF NOT EXISTS departments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) UNIQUE NOT NULL,
    code VARCHAR(50) UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- courses
CREATE TABLE IF NOT EXISTS courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    department_id UUID REFERENCES departments(id) ON DELETE SET NULL,
    course_code VARCHAR(100) UNIQUE NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    semester INTEGER,
    description TEXT,
    topics TEXT[],
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- student_courses (Many-to-many students and courses)
CREATE TABLE IF NOT EXISTS student_courses (
    student_id UUID REFERENCES student_profiles(id) ON DELETE CASCADE,
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    academic_year VARCHAR(20) NOT NULL,
    semester INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('enrolled', 'completed', 'dropped')),
    PRIMARY KEY (student_id, course_id, academic_year)
);

-- Triggers
CREATE TRIGGER update_courses_modtime
    BEFORE UPDATE ON courses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
