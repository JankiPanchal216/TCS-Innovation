from fastapi import FastAPI
from app.db.session import create_pool, close_pool
from app.routes import books

app = FastAPI(title="LibraAI API", description="AI-powered library recommendation platform")

@app.on_event("startup")
async def startup_event():
    # Initialize connection pool
    await create_pool()

@app.on_event("shutdown")
async def shutdown_event():
    # Close connection pool
    await close_pool()

# Include routers
app.include_router(books.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to LibraAI API"}
