from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

from app.services.search.semantic import SemanticSearchService
from app.services.search.keyword import KeywordSearchService
from app.services.search.hybrid import HybridSearchService
from app.services.search.models import SearchRequest, SearchFilters, SearchContext
from app.db.session import create_pool

router = APIRouter()
semantic_search_service = SemanticSearchService()
keyword_search_service = KeywordSearchService()
hybrid_search_service = HybridSearchService()

class SemanticSearchRequest(BaseModel):
    query: str = Field(..., description="The search query text")
    limit: int = Field(10, description="Maximum number of results to return")
    filters: Optional[SearchFilters] = Field(default_factory=SearchFilters)

class SearchResultItem(BaseModel):
    book_id: str
    title: str
    authors: List[str]
    description: Optional[str]
    categories: List[str]
    thumbnail: Optional[str]
    difficulty: Optional[str]
    available_copies: int
    scores: Optional[Dict[str, float]] = None
    explanation_factors: Optional[List[str]] = None
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
    personalization_latency_ms: Optional[float] = None
    total_latency_ms: float

class SearchResponse(BaseModel):
    query: str
    search_type: str
    model: Optional[str] = None
    personalization: Optional[Dict[str, bool]] = None
    results: List[SearchResultItem]
    metrics: SearchMetrics

async def log_search(user_id, query, search_type, filters, context, results_count, top_result_id, total_latency_ms):
    try:
        pool = await create_pool()
        async with pool.acquire() as conn:
            import json
            filters_json = json.dumps(filters) if filters else None
            intent_json = json.dumps({"type": "explicit"}) # Mocked intent parsing for MVP
            
            pers_enabled = False
            if context and context.get("use_profile"):
                pers_enabled = True

            await conn.execute(
                """
                INSERT INTO search_queries 
                (user_id, query, normalized_query, search_type, filters, parsed_intent, personalization_enabled, results_count, top_result_id, total_latency_ms) 
                VALUES ($1, $2, LOWER($2), $3, $4::jsonb, $5::jsonb, $6, $7, $8, $9)
                """,
                user_id, query, search_type, filters_json, intent_json, pers_enabled, results_count, top_result_id, total_latency_ms
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
        context_dict = request.context.model_dump(exclude_unset=True) if request.context else None
        profile_dict = request.context.profile if request.context and request.context.profile else None
        
        # We assume hybrid mode for unified search if mode isn't explicitly defined
        mode = getattr(request, 'mode', 'hybrid').lower()
        
        if mode == "hybrid":
            result = await hybrid_search_service.hybrid_search(
                query=request.query,
                limit=request.limit,
                filters=filters_dict,
                context=context_dict,
                profile=profile_dict
            )
            
            result["personalization"] = {
                "profile_used": context_dict.get("use_profile", False) if context_dict else False,
                "history_used": context_dict.get("use_history", False) if context_dict else False,
                "courses_used": context_dict.get("use_courses", False) if context_dict else False,
                "interests_used": context_dict.get("use_interests", False) if context_dict else False,
            }
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
            
        results = result.get("results", [])
        top_id = results[0]["book_id"] if results else None
        latency = result.get("metrics", {}).get("total_latency_ms", 0)
        
        await log_search(request.user_id, request.query, mode, filters_dict, context_dict, len(results), top_id, latency)
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
        
        results = result.get("results", [])
        top_id = results[0]["book_id"] if results else None
        latency = result.get("metrics", {}).get("total_latency_ms", 0)
        
        await log_search(None, request.query, "semantic", filters_dict, None, len(results), top_id, latency)
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
        
        results = result.get("results", [])
        top_id = results[0]["book_id"] if results else None
        latency = result.get("metrics", {}).get("total_latency_ms", 0)
        
        await log_search(None, request.query, "keyword", filters_dict, None, len(results), top_id, latency)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

