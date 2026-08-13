from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
import asyncpg
from app.db.session import get_db_connection
from app.services.library.inventory_importer import InventoryImporter

router = APIRouter(prefix="/api/library", tags=["library"])

@router.post("/inventory/upload")
async def upload_inventory(file: UploadFile = File(...), conn: asyncpg.Connection = Depends(get_db_connection)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    
    # In a real app we'd get user_id from token, using a dummy UUID for MVP testing
    # Or fetch an existing admin
    admin_id = await conn.fetchval("SELECT id FROM users WHERE role = 'admin' LIMIT 1")
    # if no admin, fallback to null (handled by schema ON DELETE SET NULL)
    
    from app.db.session import create_pool
    pool = await create_pool()
    importer = InventoryImporter(pool)
    
    try:
        stats = await importer.process_csv_upload(admin_id, file.filename, content)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/inventory/template", response_class=PlainTextResponse)
async def download_template():
    csv_content = (
        "title,author,isbn13,quantity,available_copies,department,category,location,shelf_code\n"
        "Network Security Essentials,William Stallings,9780136659225,5,5,Computer Science,Cybersecurity,Main Library,CS-A1\n"
        "Database System Concepts,Abraham Silberschatz,9780073523323,3,2,Computer Science,Databases,Main Library,CS-B2\n"
    )
    return csv_content
