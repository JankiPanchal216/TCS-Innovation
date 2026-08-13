from typing import List, Dict, Any, Set

class HistoryScorer:
    """
    Scores books based on similarity to the student's past borrowing history (10%).
    """
    def __init__(self, historical_books: List[Dict[str, Any]]):
        self.past_categories: Set[str] = set()
        self.past_authors: Set[str] = set()
        
        # Build a profile of what the user likes based on past books
        for b in historical_books:
            if "categories" in b and b["categories"]:
                for c in b["categories"]:
                    self.past_categories.add(c.lower())
            if "authors" in b and b["authors"]:
                for a in b["authors"]:
                    self.past_authors.add(a.lower())
                    
    def score(self, book: Dict[str, Any]) -> float:
        if not self.past_categories and not self.past_authors:
            return 0.0 # Cold start
            
        score = 0.0
        
        book_categories = [c.lower() for c in book.get("categories", [])] if book.get("categories") else []
        book_authors = [a.lower() for a in book.get("authors", [])] if book.get("authors") else []
        
        # If the book shares an author with a previously borrowed book, strong signal
        author_overlap = set(book_authors).intersection(self.past_authors)
        if author_overlap:
            score += 0.6
            
        # If it shares categories, also a good signal
        category_overlap = set(book_categories).intersection(self.past_categories)
        if category_overlap:
            score += 0.4
            
        return min(1.0, score)
