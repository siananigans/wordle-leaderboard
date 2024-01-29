from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from httpx import AsyncClient

from wordle_leaderboard.clients.base import BaseClient


class GoogleClient(BaseClient):
    def __init__(self, creds, base_url: str, http_client: AsyncClient):
        super().__init__(base_url, http_client)
        self.creds = creds

    def credentials(self):
        creds = self.creds
        if not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        self.creds = creds

    async def get_emails(self):
        try:
            self.credentials()
            url = self.build_url("/users/me/messages")
            resp = await self.http_client.get(
                auth=self.creds,
                url=url,
            )
            resp.raise_for_status()
            resp_data = resp.json()
            if not resp_data:
                print("No data")

            return resp_data

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")
