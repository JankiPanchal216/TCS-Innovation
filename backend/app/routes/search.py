from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

from app.services.search.semantic import SemanticSearchService
from app.services.search.keyword import KeywordSearchService
from app.services.search.hybrid import HybridSearchService
from app.db.session import create_pool

router = APIRouter()
semantic_search_service = SemanticSearchService()
keyword_search_service = KeywordSearchService()
hybrid_search_service = HybridSearchService()

class SearchFilters(BaseModel):
    difficulty: Optional[str] = None
    department: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None
    available_only: Optional[bool] = False

class SearchRequest(BaseModel):
    query: str = Field(..., description="The search query text")
    mode: Optional[str] = Field("hybrid", description="Search mode: hybrid, keyword, or semantic")
    limit: int = Field(10, description="Maximum number of results to return")
    filters: Optional[SearchFilters] = None

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
    keyword_score: Optional[float] = None
    semantic_score: Optional[float] = None
    rrf_score: Optional[float] = None
    relevance_score: Optional[float] = None
    similarity: Optional[float] = None

class SearchMetrics(BaseModel):
    keyword_latency_ms: Optional[float] = None
    semantic_embedding_latency_ms: Optional[float] = None
    semantic_db_latency_ms: Optional[float] = None
    database_search_latency_ms: Optional[float] = None
    fusion_latency_ms: Optional[float] = None
    total_latency_ms: float

class SearchResponse(BaseModel):
    query: str
    search_type: str
    model: Optional[str] = None
    results: List[SearchResultItem]
    metrics: SearchMetrics

async def log_search(user_id, query, search_type, filters, results_count):
    try:
        pool = await create_pool()
        async with pool.acquire() as conn:
            import json
            filters_json = json.dumps(filters) if filters else None
            await conn.execute(
                "INSERT INTO search_queries (user_id, query, search_type, filters, results_count) VALUES ($1, $2, $3, $4::jsonb, $5)",
                user_id, query, search_type, filters_json, results_count
            )
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Failed to log search: {e}")

@router.post("", response_model=SearchResponse)
async def unified_search(request: SearchRequest = Body(...)):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
    try:
        filters_dict = request.filters.model_dump(exclude_unset=True) if request.filters else None
        
        mode = request.mode.lower() if request.mode else "hybrid"
        
        if mode == "hybrid":
            result = await hybrid_search_service.hybrid_search(
                query=request.query,
                limit=request.limit,
                filters=filters_dict
            )
        elif mode == "keyword":
            result = await keyword_search_service.search_books_keyword(
                query=request.query,
                limit=request.limit,
                filters=filters_dict
            )
        elif mode == "semantic":
            result = await semantic_search_service.search_books_by_embedding(
                query=request.query,
                limit=request.limit,
                filters=filters_dict
            )
            result["search_type"] = "semantic"
        else:
            raise ValueError("Invalid search mode. Must be 'hybrid', 'keyword', or 'semantic'.")
            
        await log_search(None, request.query, mode, filters_dict, len(result.get("results", [])))
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.post("/semantic", response_model=SearchResponse)
async def semantic_search(request: SemanticSearchRequest = Body(...)):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
    try:
        filters_dict = request.filters.model_dump(exclude_unset=True) if request.filters else None
        
        result = await semantic_search_service.search_books_by_embedding(
            query=request.query,
            limit=request.limit,
            filters=filters_dict
        )
        result["search_type"] = "semantic"
        
        await log_search(None, request.query, "semantic", filters_dict, len(result.get("results", [])))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.post("/keyword", response_model=SearchResponse)
async def keyword_search(request: SemanticSearchRequest = Body(...)):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
    try:
        filters_dict = request.filters.model_dump(exclude_unset=True) if request.filters else None
        
        result = await keyword_search_service.search_books_keyword(
            query=request.query,
            limit=request.limit,
            filters=filters_dict
        )
        
        await log_search(None, request.query, "keyword", filters_dict, len(result.get("results", [])))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

