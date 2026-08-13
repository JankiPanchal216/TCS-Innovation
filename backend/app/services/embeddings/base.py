from abc import ABC, abstractmethod
from typing import List

class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding for a single string."""
        pass

    @abstractmethod
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of strings."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Return the name of the active embedding model."""
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        """
        Return the dimension of the embedding vectors.
        This must be determined dynamically (e.g. from the first request).
        """
        pass
