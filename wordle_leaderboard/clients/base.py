from urllib.parse import urljoin

from httpx import AsyncClient


class BaseClient:
    def __init__(self, base_url: str, http_client: AsyncClient):
        self.base_url = base_url
        self.http_client = http_client

    def build_url(self, url: str):
        return urljoin(self.base_url, url)
