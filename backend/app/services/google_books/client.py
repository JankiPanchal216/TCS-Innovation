import httpx
import asyncio
from typing import Dict, Any, List

class GoogleBooksClient:
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"
    
    def __init__(self):
        self.timeout = 10.0
    
    async def search_books(self, query: str, max_results: int = 40, start_index: int = 0) -> List[Dict[str, Any]]:
        """
        Search for books using the Google Books API.
        Handles pagination and returns a list of raw volume items.
        """
        items = []
        # Google API maxResults is 40. Loop if requested limit is higher.
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            while len(items) < max_results:
                fetch_limit = min(40, max_results - len(items))
                params = {
                    "q": query,
                    "maxResults": fetch_limit,
                    "startIndex": start_index + len(items),
                    "langRestrict": "en",
                    "printType": "books"
                }
                
                try:
                    response = await client.get(self.BASE_URL, params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    fetched_items = data.get("items", [])
                    if not fetched_items:
                        break # No more results from Google
                    
                    items.extend(fetched_items)
                    
                    # Be nice to the API
                    await asyncio.sleep(0.5)
                except httpx.HTTPError as e:
                    print(f"Error fetching from Google Books API: {e}")
                    break
                    
        return items[:max_results]
