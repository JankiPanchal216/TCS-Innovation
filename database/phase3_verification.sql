-- ============================================================================
-- Phase 3 Verification Script
-- ============================================================================

-- 1. Check if recommendations table exists and has correct columns
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'recommendations';

-- 2. Check if recommendation_feedback table exists
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'recommendation_feedback';

-- 3. Check for any generated recommendations
SELECT user_id, book_id, final_score, explanation, recommendation_engine_version
FROM recommendations
ORDER BY final_score DESC
LIMIT 5;

-- 4. Check for any recorded feedback
SELECT recommendation_id, user_id, feedback_type, created_at
FROM recommendation_feedback
ORDER BY created_at DESC
LIMIT 5;

-- 5. Verify the existence of the student profile fields needed
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'student_profiles' 
AND column_name IN ('interests', 'department', 'reading_level');
