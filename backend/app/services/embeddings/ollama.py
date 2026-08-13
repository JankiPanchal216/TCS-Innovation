import httpx
from typing import List, Optional
import asyncio

from app.config import settings
from .base import EmbeddingProvider

class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip('/')
        self.model = settings.OLLAMA_EMBEDDING_MODEL
        self.timeout = settings.OLLAMA_EMBEDDING_TIMEOUT_SECONDS
        self.max_retries = settings.OLLAMA_MAX_RETRIES
        self._dimension: Optional[int] = None

    async def _call_api_with_retry(self, client: httpx.AsyncClient, data: dict) -> httpx.Response:
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                response = await client.post(
                    f"{self.base_url}/api/embed",
                    json=data,
                    timeout=self.timeout
                )
                if response.status_code == 200:
                    return response
                else:
                    if response.status_code == 404:
                        # Model likely not installed
                        raise Exception(f"Embedding model '{self.model}' is unavailable in Ollama. Error: {response.text}")
                    else:
                        raise Exception(f"Ollama API error {response.status_code}: {response.text}")
            except httpx.RequestError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
        raise Exception(f"Failed to connect to Ollama after {self.max_retries} attempts: {str(last_exception)}")

    async def generate_embedding(self, text: str) -> List[float]:
        async with httpx.AsyncClient() as client:
            response = await self._call_api_with_retry(client, {
                "model": self.model,
                "input": text
            })
            
            data = response.json()
            if "embeddings" not in data or not data["embeddings"]:
                raise Exception("Invalid response from Ollama: no embeddings found.")
            
            embedding = data["embeddings"][0]
            
            # Validation
            if not embedding:
                raise Exception("Generated embedding is empty.")
            if not all(isinstance(x, (int, float)) for x in embedding):
                raise Exception("Generated embedding contains non-numeric values.")
                
            if self._dimension is None:
                self._dimension = len(embedding)
            elif len(embedding) != self._dimension:
                raise Exception(f"Dimension mismatch. Expected {self._dimension}, got {len(embedding)}")
                
            return embedding

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        # Ollama supports batching multiple inputs
        async with httpx.AsyncClient() as client:
            response = await self._call_api_with_retry(client, {
                "model": self.model,
                "input": texts
            })
            
            data = response.json()
            if "embeddings" not in data or len(data["embeddings"]) != len(texts):
                raise Exception("Invalid response from Ollama: incomplete embeddings returned.")
            
            embeddings = data["embeddings"]
            
            if self._dimension is None and len(embeddings) > 0:
                self._dimension = len(embeddings[0])
                
            for idx, emb in enumerate(embeddings):
                if not emb:
                    raise Exception(f"Generated embedding at index {idx} is empty.")
                if not all(isinstance(x, (int, float)) for x in emb):
                    raise Exception(f"Generated embedding at index {idx} contains non-numeric values.")
                if len(emb) != self._dimension:
                    raise Exception(f"Dimension mismatch at index {idx}. Expected {self._dimension}, got {len(emb)}")
                    
            return embeddings

    def get_model_name(self) -> str:
        return self.model

    def get_dimension(self) -> int:
        if self._dimension is None:
            raise Exception("Dimension is not known yet. Generate an embedding first.")
        return self._dimension
