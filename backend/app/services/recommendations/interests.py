from typing import List, Dict, Any

class InterestsScorer:
    """
    Scores books based on overlap with student interests (15%).
    Uses simple Jaccard-like similarity or overlap ratio.
    """
    def __init__(self, student_interests: List[str]):
        self.student_interests_lower = set(i.lower() for i in student_interests) if student_interests else set()
        
    def score(self, book: Dict[str, Any]) -> float:
        if not self.student_interests_lower:
            return 0.0
            
        book_tags = []
        if "categories" in book and book["categories"]:
            book_tags.extend([c.lower() for c in book["categories"]])
        if "subjects" in book and book["subjects"]:
            book_tags.extend([s.lower() for s in book["subjects"]])
            
        book_tags_set = set(book_tags)
        
        if not book_tags_set:
            return 0.0
            
        intersection = self.student_interests_lower.intersection(book_tags_set)
        
        # Calculate overlap relative to the book's tags (if a book has exactly the tags the user wants, score is high)
        # Or relative to user's interests. We'll use a simple ratio of how many of the student's interests are met,
        # bounded by 1.0. Actually, if any interest matches, we give a partial score.
        # Let's say score = len(intersection) / min(len(self.student_interests_lower), max(1, len(book_tags_set)))
        # A simpler approach: score = min(1.0, len(intersection) * 0.5)  # 2 matches = 1.0 score
        
        if not intersection:
            return 0.0
            
        # Give 0.5 for one match, 1.0 for 2 or more matches
        return min(1.0, len(intersection) * 0.5)
