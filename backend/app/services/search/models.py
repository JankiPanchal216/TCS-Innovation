from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SearchFilters(BaseModel):
    department: Optional[str] = None
    difficulty: Optional[str] = None
    language: Optional[str] = None
    category_ids: List[str] = Field(default_factory=list)
    author_ids: List[str] = Field(default_factory=list)
    published_after: Optional[str] = None
    published_before: Optional[str] = None
    available_only: bool = False
    course_id: Optional[str] = None

class SearchContext(BaseModel):
    use_profile: bool = True
    use_history: bool = True
    use_courses: bool = True
    use_interests: bool = True
    # Explicit profile inputs if we don't have user_id DB lookup in MVP
    profile: Optional[Dict[str, Any]] = None

class SearchRequest(BaseModel):
    query: str
    filters: SearchFilters = Field(default_factory=SearchFilters)
    context: SearchContext = Field(default_factory=SearchContext)
    limit: int = 10
    user_id: Optional[str] = None
