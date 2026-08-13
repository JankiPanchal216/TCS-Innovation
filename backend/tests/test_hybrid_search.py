import pytest
from app.services.search.hybrid import rrf_fuse

def test_rrf_fuse_basic():
    keyword_results = [
        {"book_id": "A", "keyword_score": 0.8},
        {"book_id": "B", "keyword_score": 0.7},
        {"book_id": "C", "keyword_score": 0.6}
    ]
    
    semantic_results = [
        {"book_id": "C", "similarity": 0.9},
        {"book_id": "B", "similarity": 0.8},
        {"book_id": "D", "similarity": 0.7}
    ]
    
    k = 60
    fused = rrf_fuse(keyword_results, semantic_results, k=k)
    
    # Check that C and B received contributions from both
    # Keyword: A=1, B=2, C=3
    # Semantic: C=1, B=2, D=3
    # Scores:
    # C: 1/(60+3) + 1/(60+1) = 1/63 + 1/61 = 0.01587 + 0.01639 = 0.03226
    # B: 1/(60+2) + 1/(60+2) = 2/62 = 0.03225
    # A: 1/(60+1) = 1/61 = 0.01639
    # D: 1/(60+3) = 1/63 = 0.01587
    
    # Expected order: C, B, A, D
    assert fused[0]["book_id"] == "C"
    assert fused[1]["book_id"] == "B"
    assert fused[2]["book_id"] == "A"
    assert fused[3]["book_id"] == "D"
    
    # Check that fields are correctly merged
    assert fused[0]["keyword_score"] == 0.6
    assert fused[0]["semantic_score"] == 0.9
    
def test_rrf_fuse_disjoint():
    keyword_results = [{"book_id": "A", "keyword_score": 0.8}]
    semantic_results = [{"book_id": "Z", "similarity": 0.9}]
    
    fused = rrf_fuse(keyword_results, semantic_results)
    
    assert len(fused) == 2
    # Both have rank 1 in their respective lists, so score is identical
    # The order is determined by Python's stable sort or insertion order
    ids = [f["book_id"] for f in fused]
    assert "A" in ids
    assert "Z" in ids
    
def test_rrf_fuse_empty():
    assert rrf_fuse([], []) == []
    assert len(rrf_fuse([{"book_id": "A", "keyword_score": 0.9}], [])) == 1
    assert len(rrf_fuse([], [{"book_id": "A", "similarity": 0.9}])) == 1
