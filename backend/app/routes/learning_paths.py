from fastapi import APIRouter, Depends, HTTPException
import asyncpg
from typing import List, Dict, Any

from app.db.session import get_db_connection

router = APIRouter(prefix="/api/learning-path", tags=["learning-paths"])

@router.get("/")
async def get_learning_paths(conn: asyncpg.Connection = Depends(get_db_connection)):
    """Fetch the active learning path."""
    # Mocking for now as full DB linkage requires auth + student profiles
    return {
        "id": "lp-1",
        "title": "Computer Science Foundation",
        "progress_percentage": 25,
        "time_remaining": "4 Weeks",
        "total_resources": 12,
        "current_focus": "TCP/IP Fundamentals"
    }

@router.get("/{path_id}/weeks")
async def get_learning_path_weeks(path_id: str, conn: asyncpg.Connection = Depends(get_db_connection)):
    """Fetch timeline for a learning path."""
    return [
        {
            "week_number": 1,
            "status": "CURRENT",
            "progress_percentage": 65,
            "estimated_remaining_hours": 2.5,
            "risk": "Low",
            "resources": [
                {
                    "id": "res-1",
                    "title": "Computer Networking: A Top-Down Approach",
                    "author": "Andrew S. Tanenbaum",
                    "difficulty": "Intermediate",
                    "estimated_hours": 6,
                    "match_score": 94,
                    "progress": 65,
                    "focus": "Chapters 1-3",
                    "is_locked": False,
                    "prerequisites": []
                }
            ]
        },
        {
            "week_number": 2,
            "status": "UPCOMING",
            "progress_percentage": 0,
            "estimated_remaining_hours": 8,
            "risk": "Low",
            "resources": [
                {
                    "id": "res-2",
                    "title": "Network Security Essentials",
                    "author": "William Stallings",
                    "difficulty": "Advanced",
                    "estimated_hours": 8,
                    "match_score": 88,
                    "progress": 0,
                    "focus": "Encryption",
                    "is_locked": True,
                    "prerequisites": ["TCP/IP Fundamentals"]
                }
            ]
        }
    ]

@router.get("/{path_id}/analytics")
async def get_learning_path_analytics(path_id: str, conn: asyncpg.Connection = Depends(get_db_connection)):
    """Fetch AI rationale and pacing."""
    return {
        "rationale": "Based on your assessment performance and current progress, TCP/IP Fundamentals has been prioritized before Network Security.",
        "pacing": "You are ahead of schedule.",
        "next_best_action": "Complete Chapter 3 before starting Network Security Essentials.",
        "risk_explanation": None
    }

@router.post("/{path_id}/regenerate")
async def regenerate_learning_path(path_id: str, conn: asyncpg.Connection = Depends(get_db_connection)):
    """Regenerate learning sequence."""
    return {"status": "success", "message": "Learning path optimized successfully."}
