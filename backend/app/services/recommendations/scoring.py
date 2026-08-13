from typing import List, Dict, Any

class ScoringService:
    """
    Combines various scorers to compute the final weighted recommendation score.
    Weights:
    - hybrid search score: 30%
    - academic/course relevance: 25%
    - student interests: 15%
    - borrowing/history: 10%
    - similar-student behavior: 10%
    - popularity: 5%
    - availability: 5%
    """
    
    def __init__(
        self,
        hybrid_scorer,       # Dict[str, float] of book_id to hybrid score
        academic_scorer,     # AcademicScorer
        interests_scorer,    # InterestsScorer
        history_scorer,      # HistoryScorer
        collaborative_scorer,# CollaborativeScorer
        popularity_scorer    # PopularityScorer
    ):
        self.hybrid_scores = hybrid_scorer
        self.academic_scorer = academic_scorer
        self.interests_scorer = interests_scorer
        self.history_scorer = history_scorer
        self.collaborative_scorer = collaborative_scorer
        self.popularity_scorer = popularity_scorer
        
        self.weights = {
            "hybrid": 0.30,
            "academic": 0.25,
            "interests": 0.15,
            "history": 0.10,
            "collaborative": 0.10,
            "popularity": 0.05,
            "availability": 0.05
        }
        
    def score_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        scored_candidates = []
        
        for book in candidates:
            book_id = book["book_id"]
            
            s_hybrid = self.hybrid_scores.get(book_id, 0.0)
            s_academic = self.academic_scorer.score(book)
            s_interests = self.interests_scorer.score(book)
            s_history = self.history_scorer.score(book)
            s_collab = self.collaborative_scorer.score(book)
            s_pop = self.popularity_scorer.score(book)
            
            s_avail = 1.0 if book.get("available_copies", 0) > 0 else 0.0
            
            final_score = (
                s_hybrid * self.weights["hybrid"] +
                s_academic * self.weights["academic"] +
                s_interests * self.weights["interests"] +
                s_history * self.weights["history"] +
                s_collab * self.weights["collaborative"] +
                s_pop * self.weights["popularity"] +
                s_avail * self.weights["availability"]
            )
            
            # Determine top reason
            reasons = []
            
            if s_academic > 0.5:
                reasons.append("Matches your enrolled courses")
            elif s_academic > 0:
                reasons.append("Relevant to your academic department")
                
            if s_hybrid > 0.6:
                reasons.append("Strong semantic match to your profile")
                
            if s_interests > 0.4:
                reasons.append("Matches your stated interests")
                
            if s_history > 0.5:
                reasons.append("Similar to books you previously borrowed")
                
            if s_collab > 0.3:
                reasons.append("Similar students frequently borrowed this")
                
            if s_pop > 0.7 and not reasons:
                reasons.append("Popular among all students")
                
            if s_avail > 0 and len(reasons) < 2:
                reasons.append("Currently available")
                
            if not reasons:
                reasons.append("Recommended for you")
                
            scored_candidates.append({
                "book": book,
                "final_score": round(final_score, 4),
                "component_scores": {
                    "hybrid": round(s_hybrid, 4),
                    "academic": round(s_academic, 4),
                    "interests": round(s_interests, 4),
                    "history": round(s_history, 4),
                    "collaborative": round(s_collab, 4),
                    "popularity": round(s_pop, 4),
                    "availability": round(s_avail, 4)
                },
                "availability": s_avail > 0,
                "reasons": reasons[:2] # Keep top 2 reasons
            })
            
        # Sort descending by final score
        scored_candidates.sort(key=lambda x: x["final_score"], reverse=True)
        return scored_candidates
