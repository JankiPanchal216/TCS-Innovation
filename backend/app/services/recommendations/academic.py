from typing import List, Dict, Any

class AcademicScorer:
    """
    Scores books based on academic/course relevance (25%).
    """
    def __init__(self, course_books_map: Dict[str, float]):
        # course_books_map: {book_id: relevance_score}
        # where relevance_score is the max relevance_score from course_books for the student's enrolled courses.
        self.course_books_map = course_books_map
        
    def score(self, book: Dict[str, Any]) -> float:
        book_id = book["book_id"]
        # If the book is in the course_books_map, return the relevance_score (which is 0-1)
        # Otherwise 0.0
        return float(self.course_books_map.get(book_id, 0.0))
