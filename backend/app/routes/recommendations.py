from fastapi import APIRouter, HTTPException, Query, Body, Header
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.services.recommendations.service import RecommendationService
from app.db.session import create_pool

router = APIRouter()
recommendation_service = RecommendationService()

class RecommendationFeedback(BaseModel):
    recommendation_id: str
    feedback_type: str = Field(..., description="useful, not_useful, saved, borrowed, dismissed")
    feedback_value: Optional[int] = None
    comment: Optional[str] = None

@router.get("/me")
async def get_my_recommendations(
    limit: int = Query(5, ge=1, le=20),
    user_id: str = Header(..., description="Mock auth header containing user_id")
):
    try:
        results = await recommendation_service.get_recommendations(user_id=user_id, limit=limit)
        return {"recommendations": results}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Recommendations error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations.")

@router.post("")
async def generate_recommendations_post(
    limit: int = Query(5, ge=1, le=20),
    user_id: str = Body(..., embed=True, description="The user_id to generate recommendations for")
):
    try:
        results = await recommendation_service.get_recommendations(user_id=user_id, limit=limit)
        return {"recommendations": results}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Recommendations error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations.")

@router.post("/feedback")
async def submit_feedback(
    feedback: RecommendationFeedback,
    user_id: str = Header(..., description="Mock auth header containing user_id")
):
    try:
        pool = await create_pool()
        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO recommendation_feedback 
                (recommendation_id, user_id, feedback_type, feedback_value, comment)
                VALUES ($1, $2, $3, $4, $5)
            """, 
            feedback.recommendation_id, 
            user_id, 
            feedback.feedback_type, 
            feedback.feedback_value, 
            feedback.comment)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record feedback: {e}")
