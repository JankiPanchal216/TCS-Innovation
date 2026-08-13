from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncpg

from app.db.session import get_db_connection

router = APIRouter(prefix="/api/inventory", tags=["inventory"])

class BookItem(BaseModel):
    name: str
    category: str
    availability: str = "Available"

class StructureTextRequest(BaseModel):
    text: str

@router.get("/")
async def get_inventory(conn: asyncpg.Connection = Depends(get_db_connection)):
    """Fetch books from DB or fallback list."""
    try:
        rows = await conn.fetch("SELECT id, title, subjects FROM books LIMIT 50")
        if rows:
            return [
                {
                    "id": str(r["id"]),
                    "name": r["title"],
                    "category": r["subjects"][0] if r["subjects"] else "General",
                    "availability": "Available",
                    "source": "Postgres DB",
                    "updated": "Today"
                }
                for r in rows
            ]
    except Exception:
        pass

    return [
        { "id": 1, "name": "Computer Networks", "category": "Computer Science", "availability": "Available", "source": "CSV Import", "updated": "Today" },
        { "id": 2, "name": "Operating Systems Concepts", "category": "Computer Science", "availability": "Borrowed", "source": "AI Structuring", "updated": "Today" },
        { "id": 3, "name": "Introduction to Algorithms", "category": "Mathematics", "availability": "Available", "source": "Manual Entry", "updated": "Yesterday" },
        { "id": 4, "name": "Design Patterns", "category": "Software Engineering", "availability": "Available", "source": "CSV Import", "updated": "Aug 10, 2026" }
    ]

@router.post("/structure")
async def structure_unstructured_text(req: StructureTextRequest):
    """Simulate AI structuring pipeline for raw text."""
    lines = [l.strip() for l in req.text.split('\n') if l.strip()]
    structured = []
    
    for idx, line in enumerate(lines[:5]):
        confidence = 98 - (idx * 5)
        structured.append({
            "id": idx + 1,
            "name": line,
            "category": "Extracted Domain",
            "availability": "Available" if idx % 2 == 0 else "Borrowed",
            "confidence": max(confidence, 65),
            "status": "Ready" if confidence >= 80 else "Needs Review"
        })
        
    if not structured:
        structured = [
            { "id": 1, "name": "Parsed Library Document", "category": "General", "availability": "Available", "confidence": 95, "status": "Ready" }
        ]

    return {"records": structured, "count": len(structured)}
