import asyncio
import json
import os
import math
from typing import List, Dict, Any

from app.services.search.keyword import KeywordSearchService
from app.services.search.semantic import SemanticSearchService
from app.services.search.hybrid import HybridSearchService
from app.db.session import create_pool

def is_relevant(result_categories: List[str], expected_categories: List[str]) -> bool:
    """Check if a result is relevant by matching any category."""
    # Also considering subjects/keywords mapped to categories in search result item
    for c in result_categories:
        if c in expected_categories:
            return True
    return False

def calculate_precision_at_k(results: List[Dict[str, Any]], expected_categories: List[str], k: int) -> float:
    if not results:
        return 0.0
    relevant_count = 0
    for r in results[:k]:
        if is_relevant(r.get("categories", []), expected_categories):
            relevant_count += 1
    return relevant_count / min(k, len(results))

def calculate_ndcg_at_k(results: List[Dict[str, Any]], expected_categories: List[str], k: int) -> float:
    if not results:
        return 0.0
    dcg = 0.0
    idcg = 0.0
    for i, r in enumerate(results[:k]):
        rel = 1 if is_relevant(r.get("categories", []), expected_categories) else 0
        dcg += rel / math.log2(i + 2)
        idcg += 1 / math.log2(i + 2) # Ideal assumes all k are relevant
    return dcg / idcg if idcg > 0 else 0.0

async def main():
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "tests", "data", "search_queries.json")
    with open(data_path, "r") as f:
        queries = json.load(f)
        
    keyword_service = KeywordSearchService()
    semantic_service = SemanticSearchService()
    hybrid_service = HybridSearchService()
    
    metrics = {
        "keyword": {"p5": 0, "ndcg5": 0, "latency": 0},
        "semantic": {"p5": 0, "ndcg5": 0, "latency": 0},
        "hybrid": {"p5": 0, "ndcg5": 0, "latency": 0}
    }
    
    count = 0
    
    for item in queries:
        query = item["query"]
        expected = item["relevant_categories"]
        print(f"Evaluating query: {query}")
        
        try:
            # Keyword
            kw_res = await keyword_service.search_books_keyword(query, limit=5)
            metrics["keyword"]["p5"] += calculate_precision_at_k(kw_res["results"], expected, 5)
            metrics["keyword"]["ndcg5"] += calculate_ndcg_at_k(kw_res["results"], expected, 5)
            metrics["keyword"]["latency"] += kw_res["metrics"]["total_latency_ms"]
            
            # Semantic
            sem_res = await semantic_service.search_books_by_embedding(query, limit=5)
            metrics["semantic"]["p5"] += calculate_precision_at_k(sem_res["results"], expected, 5)
            metrics["semantic"]["ndcg5"] += calculate_ndcg_at_k(sem_res["results"], expected, 5)
            metrics["semantic"]["latency"] += sem_res["metrics"]["total_latency_ms"]
            
            # Hybrid
            hyb_res = await hybrid_service.hybrid_search(query, limit=5)
            metrics["hybrid"]["p5"] += calculate_precision_at_k(hyb_res["results"], expected, 5)
            metrics["hybrid"]["ndcg5"] += calculate_ndcg_at_k(hyb_res["results"], expected, 5)
            metrics["hybrid"]["latency"] += hyb_res["metrics"]["total_latency_ms"]
            
            count += 1
        except Exception as e:
            print(f"Failed on query '{query}': {e}")
            
    if count == 0:
        print("No successful evaluations.")
        return
        
    print("\n--- Final Metrics ---")
    print(f"Total Queries Evaluated: {count}")
    print("\nKeyword Precision@5: {:.4f}".format(metrics["keyword"]["p5"] / count))
    print("Semantic Precision@5: {:.4f}".format(metrics["semantic"]["p5"] / count))
    print("Hybrid Precision@5: {:.4f}".format(metrics["hybrid"]["p5"] / count))
    
    print("\nKeyword NDCG@5: {:.4f}".format(metrics["keyword"]["ndcg5"] / count))
    print("Semantic NDCG@5: {:.4f}".format(metrics["semantic"]["ndcg5"] / count))
    print("Hybrid NDCG@5: {:.4f}".format(metrics["hybrid"]["ndcg5"] / count))
    
    print("\nAvg Keyword Latency: {:.2f}ms".format(metrics["keyword"]["latency"] / count))
    print("Avg Semantic Latency: {:.2f}ms".format(metrics["semantic"]["latency"] / count))
    print("Avg Hybrid Latency: {:.2f}ms".format(metrics["hybrid"]["latency"] / count))

if __name__ == "__main__":
    asyncio.run(main())
