from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.services.search.semantic import SemanticSearchService

router = APIRouter()
search_service = SemanticSearchService()

class SearchFilters(BaseModel):
    difficulty: Optional[str] = None
    department: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None
    available_only: Optional[bool] = False

class SemanticSearchRequest(BaseModel):
    query: str = Field(..., description="The search query text")
    limit: int = Field(10, description="Maximum number of results to return")
    filters: Optional[SearchFilters] = None

class SearchResultItem(BaseModel):
    book_id: str
    title: str
    authors: List[str]
    description: Optional[str]
    categories: List[str]
    thumbnail: Optional[str]
    difficulty: Optional[str]
    available_copies: int
    similarity: float

class SearchMetrics(BaseModel):
    embedding_latency_ms: float
    database_search_latency_ms: float
    total_latency_ms: float

class SemanticSearchResponse(BaseModel):
    query: str
    model: str
    results: List[SearchResultItem]
    metrics: SearchMetrics

@router.post("/semantic", response_model=SemanticSearchResponse)
async def semantic_search(request: SemanticSearchRequest = Body(...)):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
    try:
        filters_dict = request.filters.model_dump(exclude_unset=True) if request.filters else None
        
        result = await search_service.search_books_by_embedding(
            query=request.query,
            limit=request.limit,
            filters=filters_dict
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
