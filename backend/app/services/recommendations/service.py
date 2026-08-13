import json
from typing import List, Dict, Any

from app.db.session import create_pool
from app.services.recommendations.candidate_generator import CandidateGenerator
from app.services.recommendations.academic import AcademicScorer
from app.services.recommendations.interests import InterestsScorer
from app.services.recommendations.history import HistoryScorer
from app.services.recommendations.collaborative import CollaborativeScorer
from app.services.recommendations.popularity import PopularityScorer
from app.services.recommendations.scoring import ScoringService
from app.services.recommendations.diversity import DiversityReranker
from app.services.search.hybrid import HybridSearchService

class RecommendationService:
    def __init__(self):
        self.candidate_generator = CandidateGenerator()
        self.hybrid_service = HybridSearchService()
        self.diversity_reranker = DiversityReranker()
        
    async def get_recommendations(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        pool = await create_pool()
        async with pool.acquire() as conn:
            # 1. Fetch Student Profile & Interests
            student = await conn.fetchrow("SELECT id, interests FROM student_profiles WHERE user_id = $1", user_id)
            if not student:
                raise ValueError("Student profile not found for the given user.")
                
            student_id = student["id"]
            interests = student["interests"] or []
            
            # 2. Fetch Course Books Map (Academic)
            course_books_records = await conn.fetch("""
                SELECT cb.book_id, cb.relevance_score
                FROM student_courses sc
                JOIN course_books cb ON sc.course_id = cb.course_id
                WHERE sc.student_id = $1 AND sc.status = 'enrolled'
            """, student_id)
            course_books_map = {str(r["book_id"]): float(r["relevance_score"] or 1.0) for r in course_books_records}
            
            # 3. Fetch History Books
            history_records = await conn.fetch("""
                SELECT b.id as book_id, b.categories, b.authors
                FROM borrowings bw
                JOIN books b ON bw.book_id = b.id
                WHERE bw.student_id = $1
            """, student_id)
            history_books = [dict(r) for r in history_records]
            history_book_ids = [str(r["book_id"]) for r in history_records]
            
            # 4. Fetch Collaborative Scores
            collaborative_scores = {}
            if history_book_ids:
                # Find other students who borrowed these books, and count what else they borrowed
                collab_records = await conn.fetch("""
                    WITH similar_students AS (
                        SELECT DISTINCT student_id 
                        FROM borrowings 
                        WHERE book_id = ANY($1::uuid[]) AND student_id != $2
                    )
                    SELECT book_id, count(*) as freq
                    FROM borrowings
                    WHERE student_id IN (SELECT student_id FROM similar_students)
                    AND book_id != ALL($1::uuid[])
                    GROUP BY book_id
                """, [history_book_ids, student_id])
                
                max_freq = max([r["freq"] for r in collab_records]) if collab_records else 1
                for r in collab_records:
                    collaborative_scores[str(r["book_id"])] = float(r["freq"]) / max_freq
                    
            # 5. Fetch Popularity Scores
            pop_records = await conn.fetch("""
                SELECT book_id, count(*) as freq 
                FROM borrowings 
                GROUP BY book_id
            """)
            max_pop = max([r["freq"] for r in pop_records]) if pop_records else 1
            popularity_scores = {str(r["book_id"]): float(r["freq"]) / max_pop for r in pop_records}
            
        # 6. Fetch Hybrid Scores
        query_text = " ".join(interests)
        hybrid_scores = {}
        if query_text:
            try:
                # We fetch a larger candidate pool from hybrid search to get scores
                hybrid_res = await self.hybrid_service.hybrid_search(query_text, limit=100)
                for item in hybrid_res.get("results", []):
                    hybrid_scores[item["book_id"]] = item.get("relevance_score", 0.0)
            except Exception:
                # If hybrid search fails (e.g., no embeddings), we gracefully fallback to 0.0
                pass
                
        # 7. Initialize Scorers
        academic_scorer = AcademicScorer(course_books_map)
        interests_scorer = InterestsScorer(interests)
        history_scorer = HistoryScorer(history_books)
        collab_scorer = CollaborativeScorer(collaborative_scores)
        pop_scorer = PopularityScorer(popularity_scores)
        
        scoring_service = ScoringService(
            hybrid_scores,
            academic_scorer,
            interests_scorer,
            history_scorer,
            collab_scorer,
            pop_scorer
        )
        
        # 8. Generate Candidates and Score
        candidates = await self.candidate_generator.get_candidates(user_id)
        scored_candidates = scoring_service.score_candidates(candidates)
        
        # 9. Rerank for Diversity
        final_recommendations = self.diversity_reranker.rerank(scored_candidates, limit)
        
        # 10. Persist Recommendations
        await self._persist_recommendations(user_id, final_recommendations)
        
        # Return formatted API response
        return self._format_response(final_recommendations)
        
    async def _persist_recommendations(self, user_id: str, recommendations: List[Dict[str, Any]]):
        pool = await create_pool()
        async with pool.acquire() as conn:
            # Optional: Delete previous recommendations for the user to keep it clean
            await conn.execute("DELETE FROM recommendations WHERE user_id = $1", user_id)
            
            for item in recommendations:
                book_id = item["book"]["book_id"]
                score = item["final_score"]
                components = item["component_scores"]
                reasons = item["reasons"]
                explanation = ". ".join(reasons)
                
                await conn.execute("""
                    INSERT INTO recommendations (
                        user_id, book_id, final_score, semantic_score, academic_score, 
                        interest_score, history_score, popularity_score, 
                        explanation, recommendation_engine_version
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, 'v1')
                """, 
                user_id, 
                book_id, 
                score,
                components["hybrid"],
                components["academic"],
                components["interests"],
                components["history"],
                components["popularity"],
                explanation
                )
                
    def _format_response(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        response = []
        for item in recommendations:
            response.append({
                "book": item["book"],
                "score_percentage": round(item["final_score"] * 100, 1),
                "component_scores": item["component_scores"],
                "availability": item["availability"],
                "reasons": item["reasons"]
            })
        return response
