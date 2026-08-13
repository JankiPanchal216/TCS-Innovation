import asyncio
from app.config import settings
from .ollama import OllamaEmbeddingProvider
from .service import EmbeddingService

async def main():
    provider = OllamaEmbeddingProvider()
    service = EmbeddingService(provider=provider)
    
    status = await service.get_status()
    
    print("Total books:")
    print(status["total_books"])
    print("\nEmbedded:")
    print(status["embedded"])
    print("\nMissing:")
    print(status["missing"])
    print("\nStale:")
    print(status["stale"])
    print("\nModel:")
    print(status["model"])
    print("\nDimensions:")
    print(status["dimensions"] if status["dimensions"] is not None else "ACTUAL")
    print("\nLast updated:")
    print(status["last_updated"] if status["last_updated"] is not None else "ACTUAL")
    print("\nFailed:")
    print(status["failed"])

if __name__ == "__main__":
    asyncio.run(main())
