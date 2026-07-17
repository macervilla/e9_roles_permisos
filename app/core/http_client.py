from httpx import AsyncClient, Timeout


class HttpClient:
    def __init__(self):
        self.client = AsyncClient(
            timeout=Timeout(5.0),
            headers={"Accept": "application/json"},
        )

    async def get(self, url: str, params: dict | None = None):
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()


http_client = HttpClient()
