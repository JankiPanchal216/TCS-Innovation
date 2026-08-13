import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.search.semantic import SemanticSearchService

class MockProvider:
    def get_model_name(self):
        return "mock-model"
        
    async def generate_embedding(self, query):
        return [0.1, 0.2, 0.3]

@pytest.fixture
def mock_pool():
    pool = AsyncMock()
    conn = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = conn
    return pool, conn

@pytest.mark.asyncio
async def test_search_books_by_embedding(mock_pool):
    pool, conn = mock_pool
    
    # Setup connection fetch returns
    conn.fetchval.return_value = True # Model exists
    
    # Mock records
    conn.fetch.return_value = [
        {
            "book_id": "123",
            "title": "Mock Book",
            "authors": ["Author A"],
            "description": "Desc",
            "categories": ["Cat1"],
            "thumbnail": None,
            "difficulty": "beginner",
            "availability": True,
            "similarity": 0.95
        }
    ]
    
    with patch('app.services.search.semantic.create_pool', return_value=pool):
        service = SemanticSearchService()
        service.provider = MockProvider()
        
        result = await service.search_books_by_embedding("test query", limit=5)
        
        assert result["query"] == "test query"
        assert result["model"] == "mock-model"
        assert len(result["results"]) == 1
        
        item = result["results"][0]
        assert item["book_id"] == "123"
        assert item["title"] == "Mock Book"
        assert item["similarity"] == 0.95
        assert item["available_copies"] == 1

@pytest.mark.asyncio
async def test_search_model_mismatch(mock_pool):
    pool, conn = mock_pool
    
    # Setup connection fetch returns
    conn.fetchval.return_value = False # Model doesn't exist
    
    with patch('app.services.search.semantic.create_pool', return_value=pool):
        service = SemanticSearchService()
        service.provider = MockProvider()
        
        with pytest.raises(ValueError, match="No embeddings found for model"):
            await service.search_books_by_embedding("test query", limit=5)
