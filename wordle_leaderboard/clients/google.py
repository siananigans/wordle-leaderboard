from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from httpx import AsyncClient, HTTPStatusError

from wordle_leaderboard.clients.base import BaseClient


class GoogleCredentialsError(Exception):
    status_code = 401
    detail = "Google cannot authenticate your credentials."


class GoogleClient(BaseClient):
    def __init__(self, creds, base_url: str, http_client: AsyncClient):
        super().__init__(base_url, http_client)
        self.creds = creds

    def credentials(self):
        try:
            creds = self.creds
            if not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
            self.creds = creds
        except Exception:
            raise GoogleCredentialsError()

    async def get_emails(self):
        try:
            self.credentials()
            url = self.build_url("users/me/messages")
            resp = await self.http_client.get(
                headers={"Authorization": "Bearer " + self.creds.token},
                url=url,
            )
            resp.raise_for_status()
            resp_data = resp.json()
            if not resp_data:
                print("No data")
            return resp_data

        except HttpError as error:
            # TODO - Handle errors from gmail API.
            print(f"An error occurred: {error}")
            raise error

    async def get_emails_build(self):
        self.credentials()
        gmail = build("gmail", "v1", credentials=self.creds)
        results = gmail.users().threads().list(userId="me").execute()
        emails = results.get("threads", [])
        return emails
