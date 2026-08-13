from typing import Dict, Any

class CollaborativeScorer:
    """
    Scores books based on similar-student behavior (10%).
    """
    def __init__(self, collaborative_scores: Dict[str, float]):
        # collaborative_scores: {book_id: normalized_score}
        # where normalized_score is based on how many similar students borrowed the book
        self.collaborative_scores = collaborative_scores
        
    def score(self, book: Dict[str, Any]) -> float:
        book_id = book["book_id"]
        return float(self.collaborative_scores.get(book_id, 0.0))
