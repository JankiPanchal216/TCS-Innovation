import time
import logging
from typing import List, Dict, Any, Optional

from app.services.search.keyword import KeywordSearchService
from app.services.search.semantic import SemanticSearchService

logger = logging.getLogger(__name__)

def rrf_fuse(keyword_results: List[Dict[str, Any]], semantic_results: List[Dict[str, Any]], k: int = 60) -> List[Dict[str, Any]]:
    """
    Implements Reciprocal Rank Fusion (RRF).
    RRF_score(d) = 1 / (k + rank_keyword(d)) + 1 / (k + rank_semantic(d))
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
        filters: Optional[Dict[str, Any]] = None
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
        
        # Apply final limit
        final_results = fused_results[:limit]
        
        fusion_latency_ms = (time.time() - fusion_start) * 1000
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
                "total_latency_ms": round(total_latency_ms, 2)
            }
        }
