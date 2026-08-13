import datetime
from typing import Dict, Any, List, Optional, Tuple

def normalize_author_name(name: str) -> str:
    """Normalize author name to avoid duplicates."""
    if not name:
        return "Unknown Author"
    # Basic normalization: title case, strip extra spaces
    return " ".join(name.strip().split()).title()

def normalize_category(category: str) -> str:
    """Normalize category name."""
    if not category:
        return "Uncategorized"
    
    # Standardize common categories
    cat = " ".join(category.strip().split()).title()
    
    # Handle hierarchical or combined categories from Google (e.g., "Computers / Artificial Intelligence")
    parts = [p.strip() for p in cat.split("/")]
    
    # Return the most specific category or just standard format
    # For now, we'll return the final part as the primary category 
    # but keep the structure in mind. We'll map the last part.
    return parts[-1]

def determine_difficulty(categories: List[str], title: str, description: str) -> str:
    """Heuristic to determine book difficulty."""
    text = (title + " " + (description or "")).lower()
    
    if "advanced" in text or "expert" in text or "theory" in text or "analysis" in text:
        return "advanced"
    elif "introduction" in text or "basics" in text or "fundamentals" in text or "beginner" in text or "for dummies" in text:
        return "beginner"
    else:
        return "intermediate"

def extract_isbns(identifiers: List[Dict[str, str]]) -> Tuple[Optional[str], Optional[str]]:
    """Extract ISBN-10 and ISBN-13 from industryIdentifiers."""
    isbn10 = None
    isbn13 = None
    if not identifiers:
        return None, None
        
    for identifier in identifiers:
        if identifier.get("type") == "ISBN_10":
            isbn10 = identifier.get("identifier")
        elif identifier.get("type") == "ISBN_13":
            isbn13 = identifier.get("identifier")
            
    return isbn10, isbn13

def parse_published_date(date_str: str) -> Optional[datetime.date]:
    """Parse Google Books date format (YYYY, YYYY-MM, or YYYY-MM-DD)."""
    if not date_str:
        return None
    try:
        parts = date_str.split('-')
        if len(parts) == 1:
            return datetime.date(int(parts[0]), 1, 1)
        elif len(parts) == 2:
            return datetime.date(int(parts[0]), int(parts[1]), 1)
        elif len(parts) >= 3:
            return datetime.date(int(parts[0]), int(parts[1]), int(parts[2][:2])) # Handle potential time components safely
    except Exception:
        return None
    return None

def map_volume_to_book(raw_volume: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Map a raw Google Books volume to our database dictionary structure.
    Returns None if the book is missing required fields (id, title).
    """
    volume_id = raw_volume.get("id")
    volume_info = raw_volume.get("volumeInfo", {})
    
    title = volume_info.get("title")
    
    if not volume_id or not title:
        return None
        
    # Identifiers
    isbn10, isbn13 = extract_isbns(volume_info.get("industryIdentifiers", []))
    
    # Dates
    pub_date_str = volume_info.get("publishedDate")
    pub_date = parse_published_date(pub_date_str)
    
    # Images
    image_links = volume_info.get("imageLinks", {})
    thumbnail = image_links.get("thumbnail") or image_links.get("smallThumbnail")
    
    # Authors and Categories
    raw_authors = volume_info.get("authors", [])
    raw_categories = volume_info.get("categories", [])
    
    normalized_authors = [normalize_author_name(a) for a in raw_authors]
    normalized_categories = [normalize_category(c) for c in raw_categories]
    
    # Calculate derived fields
    description = volume_info.get("description", "")
    difficulty = determine_difficulty(normalized_categories, title, description)
    
    # Extract searchable keywords from categories and title
    keywords = list(set([word.lower() for word in title.split() if len(word) > 3]))
    
    return {
        "google_book_id": volume_id,
        "isbn10": isbn10,
        "isbn13": isbn13,
        "title": title,
        "subtitle": volume_info.get("subtitle"),
        "description": description,
        "publisher": volume_info.get("publisher"),
        "published_date": pub_date,
        "language": volume_info.get("language", "en"),
        "page_count": volume_info.get("pageCount"),
        "thumbnail_url": thumbnail,
        "preview_url": volume_info.get("previewLink"),
        "difficulty": difficulty,
        "subjects": normalized_categories,
        "keywords": keywords,
        # Keep track of authors for relation building later
        "_extracted_authors": normalized_authors,
        "_extracted_categories": normalized_categories
    }
