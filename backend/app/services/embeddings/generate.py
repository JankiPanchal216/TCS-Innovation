import argparse
import asyncio
import sys

from app.config import settings
from .ollama import OllamaEmbeddingProvider
from .service import EmbeddingService

async def main():
    parser = argparse.ArgumentParser(description="Generate embeddings for books.")
    parser.add_argument("--limit", type=int, help="Limit the number of books to process")
    parser.add_argument("--batch-size", type=int, default=settings.OLLAMA_EMBEDDING_BATCH_SIZE, help="Batch size for embedding generation")
    parser.add_argument("--model", type=str, default=settings.OLLAMA_EMBEDDING_MODEL, help="Embedding model to use")
    parser.add_argument("--force", action="store_true", help="Regenerate all embeddings")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be embedded without modifying the database")
    
    args = parser.parse_args()
    
    if args.model:
        settings.OLLAMA_EMBEDDING_MODEL = args.model
        
    provider = OllamaEmbeddingProvider()
    service = EmbeddingService(provider=provider, batch_size=args.batch_size)
    
    print(f"Starting embedding generation using model: {settings.OLLAMA_EMBEDDING_MODEL}")
    
    if args.dry_run:
        from app.db.session import create_pool
        pool = await create_pool()
        async with pool.acquire() as conn:
            books = await service._get_books_needing_embeddings(conn, limit=args.limit, force=args.force)
            print(f"Dry run: {len(books)} books need embeddings.")
            if books:
                print("First 3 books to process:")
                for b in books[:3]:
                    print(f" - {b['title']}")
        return

    stats = await service.process_embeddings(limit=args.limit, force=args.force)
    
    print("\n--- Embedding Generation Complete ---")
    print(f"Model: {stats['model']}")
    print(f"Dimensions: {stats['dimensions']}")
    print(f"Books Processed: {stats['books_processed']}")
    print(f"Successful: {stats['successful_embeddings']}")
    print(f"Failed: {stats['failed_embeddings']}")
    print(f"Elapsed Time: {stats['elapsed_time']:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
