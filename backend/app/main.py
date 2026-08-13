from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import create_pool, close_pool
from app.routes import books, learning_paths, copilot, inventory

app = FastAPI(title="LibraAI API", description="AI-powered library recommendation platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(learning_paths.router)
app.include_router(copilot.router)
app.include_router(inventory.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to LibraAI API"}
