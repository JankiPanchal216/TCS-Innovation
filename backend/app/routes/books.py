from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncpg

from app.db.session import get_db_connection
from app.services.google_books.importer import GoogleBooksImporter

router = APIRouter(prefix="/api/books", tags=["books"])

class ImportRequest(BaseModel):
    query: str
    limit: int = 50

@router.post("/import")
async def import_books(request: ImportRequest, conn: asyncpg.Connection = Depends(get_db_connection)):
    """
    Import books from Google Books API.
    Protected endpoint (add auth later).
    """
    # Create importer but inject the existing request connection rather than the full pool.
    # To keep it simple, we can adapt the importer to accept a pool or a single connection.
    # Our GoogleBooksImporter takes a pool by default, but we can wrap the conn in a dummy pool interface 
    # OR we can just instantiate a new pool or pass the pool explicitly.
    # The safest way is to just let the importer use the global pool.
    
    from app.db.session import create_pool
    pool = await create_pool()
    importer = GoogleBooksImporter(pool)
    
    try:
        await importer.run_query(request.query, limit=request.limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {
        "success": True,
        "query": request.query,
        "fetched": importer.stats["fetched"],
        "inserted": importer.stats["inserted"],
        "updated": importer.stats["updated"],
        "skipped": importer.stats["skipped"]
    }
