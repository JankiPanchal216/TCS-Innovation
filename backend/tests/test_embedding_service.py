import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from app.services.embeddings.service import EmbeddingService
from app.services.embeddings.base import EmbeddingProvider

class MockEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        self.dim = 3
        
    async def generate_embedding(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]
        
    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        return [[0.1, 0.2, 0.3] for _ in texts]
        
    def get_model_name(self) -> str:
        return "mock-model"
        
    def get_dimension(self) -> int:
        return self.dim

@pytest.mark.asyncio
async def test_process_embeddings():
    provider = MockEmbeddingProvider()
    service = EmbeddingService(provider=provider, batch_size=2)
    
    # Mock the internal connection and queries
    mock_conn = AsyncMock()
    mock_pool = AsyncMock()
    
    # Set up the context manager for acquire
    mock_acquire_ctx = AsyncMock()
    mock_acquire_ctx.__aenter__.return_value = mock_conn
    mock_pool.acquire.return_value = mock_acquire_ctx
    
    # Set up transaction
    mock_tx = AsyncMock()
    mock_conn.transaction.return_value = mock_tx
    
    # Patch create_pool to return our mock pool
    import app.services.embeddings.service
    app.services.embeddings.service.create_pool = AsyncMock(return_value=mock_pool)
    
    # Mock _get_books_needing_embeddings
    service._get_books_needing_embeddings = AsyncMock(return_value=[
        {"id": "uuid1", "title": "Book 1", "subtitle": None, "authors": None, "subjects": None, "categories": None, "description": "Desc 1"},
        {"id": "uuid2", "title": "Book 2", "subtitle": None, "authors": None, "subjects": None, "categories": None, "description": "Desc 2"},
        {"id": "uuid3", "title": "Book 3", "subtitle": None, "authors": None, "subjects": None, "categories": None, "description": "Desc 3"}
    ])
    
    # Mock index existence check to true
    mock_conn.fetchval.return_value = True
    
    stats = await service.process_embeddings()
    
    assert stats["books_processed"] == 3
    assert stats["successful_embeddings"] == 3
    assert stats["failed_embeddings"] == 0
    assert stats["model"] == "mock-model"
    assert stats["dimensions"] == 3
    
    # We expect 2 batches: 2 elements and 1 element
    # That means 2 transactions and 3 update statements executed
    assert mock_conn.execute.call_count == 3
