import time
import logging
from typing import List, Dict, Any, Optional

from app.services.search.keyword import KeywordSearchService
from app.services.search.semantic import SemanticSearchService

logger = logging.getLogger(__name__)

def rrf_fuse(keyword_results: List[Dict[str, Any]], semantic_results: List[Dict[str, Any]], k: int = 60) -> List[Dict[str, Any]]:
    """
    Implements Reciprocal Rank Fusion (RRF).
    """
    fused_scores = {}
    docs = {}
    
    # Process Keyword results
    for rank, item in enumerate(keyword_results, 1):
        book_id = item["book_id"]
        if book_id not in docs:
            docs[book_id] = item
        
        score = 1.0 / (k + rank)
        if book_id not in fused_scores:
            fused_scores[book_id] = {"keyword_score": item["keyword_score"], "semantic_score": 0.0, "rrf_score": score, "keyword_rank": rank, "semantic_rank": 0}
        else:
            fused_scores[book_id]["rrf_score"] += score
            fused_scores[book_id]["keyword_score"] = item["keyword_score"]
            fused_scores[book_id]["keyword_rank"] = rank

    # Process Semantic results
    for rank, item in enumerate(semantic_results, 1):
        book_id = item["book_id"]
        if book_id not in docs:
            docs[book_id] = item
            
        score = 1.0 / (k + rank)
        if book_id not in fused_scores:
            fused_scores[book_id] = {"keyword_score": 0.0, "semantic_score": item["similarity"], "rrf_score": score, "keyword_rank": 0, "semantic_rank": rank}
        else:
            fused_scores[book_id]["rrf_score"] += score
            fused_scores[book_id]["semantic_score"] = item["similarity"]
            fused_scores[book_id]["semantic_rank"] = rank

    # Format the fused results
    final_results = []
    # Maximum possible RRF score is when rank=1 for both: 1/(k+1) + 1/(k+1) = 2/(k+1)
    max_possible_score = 2.0 / (k + 1)
    
    for book_id, scores in fused_scores.items():
        doc = docs[book_id].copy()
        
        # Build the final document
        doc["keyword_score"] = scores["keyword_score"]
        doc["semantic_score"] = scores["semantic_score"]
        doc["rrf_score"] = round(scores["rrf_score"], 6)
        
        # Normalize score for the UI
        normalized = scores["rrf_score"] / max_possible_score
        doc["relevance_score"] = round(normalized, 4)
        
        # Clean up fields only present in one but not the other if needed, 
        # but both services return essentially the same structure.
        doc.pop("similarity", None)
        doc.pop("rank", None)
        
        final_results.append(doc)
        
    # Sort descending by RRF score
    final_results.sort(key=lambda x: x["rrf_score"], reverse=True)
    return final_results

def apply_personalization(fused_results: List[Dict[str, Any]], context: Dict[str, Any], profile: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    personalized_score = 0.50 * normalized_rrf_score + 0.15 * academic_relevance + 0.15 * interest_match + 0.10 * history_match + 0.05 * popularity + 0.05 * availability_signal
    """
    if not profile:
        profile = {}
    
    courses = [c.lower() for c in profile.get('current_courses', [])]
    interests = [i.lower() for i in profile.get('interests', [])]
    department = profile.get('department', '').lower()

    for doc in fused_results:
        rrf = doc.get("relevance_score", 0.0)
        
        # Calculate soft signals
        title_desc = (doc.get("title", "") + " " + doc.get("description", "")).lower()
        cats = " ".join([c.lower() for c in doc.get("categories", [])])
        
        academic_score = 0.0
        if context.get("use_courses", False) and courses:
            if any(c in title_desc or c in cats for c in courses):
                academic_score = 1.0
        elif department and (department in cats or department in title_desc):
            academic_score = 0.5

        interest_score = 0.0
        if context.get("use_interests", False) and interests:
            if any(i in title_desc or i in cats for i in interests):
                interest_score = 1.0

        history_score = 0.0 # Mocked for MVP unless we join with interactions
        popularity_score = 0.5 # Mocked base popularity

        availability_score = 1.0 if doc.get("available_copies", 0) > 0 else 0.0
        
        final_score = (
            (0.50 * rrf) +
            (0.15 * academic_score) +
            (0.15 * interest_score) +
            (0.10 * history_score) +
            (0.05 * popularity_score) +
            (0.05 * availability_score)
        )
        
        doc["scores"] = {
            "keyword_score": doc.get("keyword_score", 0),
            "semantic_score": doc.get("semantic_score", 0),
            "rrf_score": rrf,
            "academic_score": round(academic_score, 4),
            "interest_score": round(interest_score, 4),
            "history_score": round(history_score, 4),
            "popularity_score": round(popularity_score, 4),
            "final_score": round(final_score, 4)
        }
        
        # Add explanation factors
        factors = []
        if academic_score > 0: factors.append("Matches your academic courses/department")
        if interest_score > 0: factors.append("Matches your profile interests")
        if availability_score > 0: factors.append("Currently available in library")
        if rrf > 0.5: factors.append("Highly relevant to search terms")
        doc["explanation_factors"] = factors
        
    fused_results.sort(key=lambda x: x["scores"]["final_score"], reverse=True)
    return fused_results


class HybridSearchService:
    def __init__(self, k: int = 60, candidate_multiplier: int = 3):
        self.keyword_service = KeywordSearchService()
        self.semantic_service = SemanticSearchService()
        self.k = k
        self.candidate_multiplier = candidate_multiplier
        
    async def hybrid_search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        
        start_time = time.time()
        
        candidate_limit = limit * self.candidate_multiplier
        
        # It's usually faster to run both concurrently, but we can do sequentially for simplicity
        # or use asyncio.gather for performance.
        import asyncio
        
        kw_task = self.keyword_service.search_books_keyword(query, candidate_limit, filters)
        sem_task = self.semantic_service.search_books_by_embedding(query, candidate_limit, filters)
        
        kw_result, sem_result = await asyncio.gather(kw_task, sem_task, return_exceptions=True)
        
        keyword_results = []
        semantic_results = []
        
        kw_latency = 0
        sem_latency = 0
        sem_db_latency = 0
        sem_emb_latency = 0
        
        if not isinstance(kw_result, Exception):
            keyword_results = kw_result.get("results", [])
            kw_latency = kw_result.get("metrics", {}).get("keyword_latency_ms", 0)
        else:
            logger.error(f"Keyword search failed: {kw_result}")
            
        if not isinstance(sem_result, Exception):
            semantic_results = sem_result.get("results", [])
            sem_latency = sem_result.get("metrics", {}).get("total_latency_ms", 0)
            sem_emb_latency = sem_result.get("metrics", {}).get("embedding_latency_ms", 0)
            sem_db_latency = sem_result.get("metrics", {}).get("database_search_latency_ms", 0)
        else:
            logger.error(f"Semantic search failed: {sem_result}")
            
        fusion_start = time.time()
        
        fused_results = rrf_fuse(keyword_results, semantic_results, k=self.k)
        
        personalization_start = time.time()
        if context and profile:
            fused_results = apply_personalization(fused_results, context, profile)
        personalization_latency_ms = (time.time() - personalization_start) * 1000
        
        # Apply final limit
        final_results = fused_results[:limit]
        
        fusion_latency_ms = (time.time() - fusion_start) * 1000 - personalization_latency_ms
        total_latency_ms = (time.time() - start_time) * 1000
        
        return {
            "query": query,
            "search_type": "hybrid",
            "results": final_results,
            "metrics": {
                "keyword_latency_ms": round(kw_latency, 2),
                "semantic_embedding_latency_ms": round(sem_emb_latency, 2),
                "semantic_db_latency_ms": round(sem_db_latency, 2),
                "fusion_latency_ms": round(fusion_latency_ms, 2),
                "personalization_latency_ms": round(personalization_latency_ms if context else 0, 2),
                "total_latency_ms": round(total_latency_ms, 2)
            }
        }
