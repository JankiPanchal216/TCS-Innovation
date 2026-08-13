from typing import List, Dict, Any

class DiversityReranker:
    """
    Reranks scored candidates to ensure diversity.
    Constraint: max 2 books from the same category in top results.
    """
    def __init__(self, max_per_category: int = 2):
        self.max_per_category = max_per_category
        
    def rerank(self, scored_candidates: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        final_list = []
        category_counts = {}
        
        for candidate in scored_candidates:
            if len(final_list) >= limit:
                break
                
            book = candidate["book"]
            categories = book.get("categories") or []
            
            # Check if adding this book violates the diversity constraint
            can_add = True
            for cat in categories:
                cat_lower = cat.lower()
                if category_counts.get(cat_lower, 0) >= self.max_per_category:
                    can_add = False
                    break
                    
            if can_add:
                final_list.append(candidate)
                # Update counts
                for cat in categories:
                    cat_lower = cat.lower()
                    category_counts[cat_lower] = category_counts.get(cat_lower, 0) + 1
                    
        return final_list
