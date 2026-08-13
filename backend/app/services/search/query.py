import re

def normalize_query(query: str) -> str:
    """
    Normalizes a search query for consistent keyword and semantic search.
    - Trims whitespace
    - Normalizes repeated spaces
    - Preserves technical tokens (like TCP/IP, C++)
    """
    if not query:
        return ""
        
    # Trim and reduce multiple spaces
    normalized = query.strip()
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # We could do more advanced stemming or punctuation removal here,
    # but the requirement is to preserve technical terms like TCP/IP, DBMS, etc.
    # PostgreSQL's websearch_to_tsquery handles standard punctuation well,
    # so we'll leave it mostly as-is for the FTS engine.
    
    # Enforce maximum query length (e.g. 200 chars to prevent DoS via massive queries)
    if len(normalized) > 200:
        normalized = normalized[:200]
        
    return normalized
