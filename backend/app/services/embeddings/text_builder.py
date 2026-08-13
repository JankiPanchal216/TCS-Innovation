import re

def build_embedding_text(book: dict) -> str:
    """
    Converts a book record into a high-quality semantic representation.
    """
    parts = []
    
    # Title
    if book.get("title"):
        title_text = f"Title: {book['title']}"
        if book.get("subtitle"):
            title_text += f" - {book['subtitle']}"
        parts.append(title_text)
        
    # Authors
    if book.get("authors"):
        authors_list = book["authors"]
        if isinstance(authors_list, list):
            authors_str = ", ".join(authors_list)
        else:
            authors_str = str(authors_list)
        if authors_str.strip():
            parts.append(f"Authors: {authors_str}")
            
    # Subjects
    if book.get("subjects"):
        subjects_list = book["subjects"]
        if isinstance(subjects_list, list):
            subjects_str = ", ".join(subjects_list)
        else:
            subjects_str = str(subjects_list)
        if subjects_str.strip():
            parts.append(f"Subjects: {subjects_str}")
            
    # Categories
    if book.get("categories"):
        categories_list = book["categories"]
        if isinstance(categories_list, list):
            categories_str = ", ".join(categories_list)
        else:
            categories_str = str(categories_list)
        if categories_str.strip():
            parts.append(f"Categories: {categories_str}")
            
    # Description
    if book.get("description"):
        desc = book["description"]
        # Normalize whitespace
        desc = re.sub(r'\s+', ' ', desc).strip()
        # Truncate extremely long descriptions (e.g. > 1500 chars)
        if len(desc) > 1500:
            desc = desc[:1497] + "..."
        if desc:
            parts.append(f"Description: {desc}")
            
    return "\n\n".join(parts)
