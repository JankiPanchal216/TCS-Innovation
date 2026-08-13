import pytest
from app.services.search.hybrid import apply_personalization

def test_apply_personalization():
    fused_results = [
        {
            "book_id": "1",
            "title": "Computer Networks",
            "description": "A book about networking",
            "categories": ["Computer Science", "Networking"],
            "relevance_score": 0.8,
            "available_copies": 2
        },
        {
            "book_id": "2",
            "title": "Cybersecurity Basics",
            "description": "Intro to infosec",
            "categories": ["Computer Science", "Cybersecurity"],
            "relevance_score": 0.7,
            "available_copies": 0
        }
    ]
    
    context = {
        "use_profile": True,
        "use_courses": True,
        "use_interests": True
    }
    
    profile = {
        "department": "Computer Science",
        "current_courses": ["Computer Networks"],
        "interests": ["Cybersecurity"]
    }
    
    result = apply_personalization(fused_results, context, profile)
    
    assert len(result) == 2
    # Both get 0.5 (department). Book 1 gets +1.0 academic (course). Book 2 gets +1.0 interest.
    # Book 1 has availability (+1.0) and higher base RRF.
    # Book 1 final should be strictly greater than Book 2.
    assert result[0]["book_id"] == "1"
    assert "scores" in result[0]
    assert result[0]["scores"]["academic_score"] == 1.0
    assert result[1]["scores"]["interest_score"] == 1.0
    assert result[1]["scores"]["academic_score"] == 0.5
