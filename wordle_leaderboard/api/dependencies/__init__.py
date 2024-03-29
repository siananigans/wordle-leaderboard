from fastapi import Depends
from httpx import AsyncClient, AsyncHTTPTransport
from google_auth_oauthlib.flow import InstalledAppFlow

from wordle_leaderboard.clients.google import GoogleClient
from wordle_leaderboard.settings import Settings, get_settings

CREDS = None


def get_google_credentials(settings: Settings = Depends(get_settings)):
    global CREDS
    if not CREDS:
        data = dict(
            client_id=settings.google_client_id,
            project_id=settings.google_project_id,
            auth_uri=settings.google_auth_uri,
            token_uri=settings.google_token_uri,
            auth_provider_x509_cert_url=settings.google_auth_provider_x509_cert_url,
            client_secret=settings.google_client_secret,
            redirect_uris=settings.google_redirect_uris,
        )
        google_creds_config = dict(installed=data)
        scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
        try:
            flow = InstalledAppFlow.from_client_config(google_creds_config, scopes)
            flow.redirect_uri = "http://localhost:8000/token"
            # TODO Map creds object to data class
            """
            {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            """
            creds = flow.run_local_server(port=0, timeout_seconds=60)
            CREDS = creds
        except Exception as e:
            print(e)
    return CREDS


async def get_http_client():
    transport = AsyncHTTPTransport(retries=2)
    async with AsyncClient(transport=transport) as client:
        yield client


def get_google_client(
    settings: Settings = Depends(get_settings),
    http_client: AsyncClient = Depends(get_http_client),
    creds=Depends(get_google_credentials),
):
    return GoogleClient(
        base_url=settings.google_base_url, http_client=http_client, creds=creds
    )
