from typing import Dict, Any

class PopularityScorer:
    """
    Scores books based on overall popularity (5%).
    """
    def __init__(self, popularity_scores: Dict[str, float]):
        # popularity_scores: {book_id: normalized_score}
        # where normalized_score is based on global borrow counts or interactions
        self.popularity_scores = popularity_scores
        
    def score(self, book: Dict[str, Any]) -> float:
        book_id = book["book_id"]
        return float(self.popularity_scores.get(book_id, 0.0))
