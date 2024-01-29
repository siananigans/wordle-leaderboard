from fastapi import APIRouter, Depends

from wordle_leaderboard.clients.google import GoogleClient
from wordle_leaderboard.api.dependencies import get_google_client


router = APIRouter(tags=["google"])


@router.get(
    "/emails",
    operation_id="get_emails",
)
async def handle_get_emails(
    google_client: GoogleClient = Depends(get_google_client),
):
    try:
        emails = await google_client.get_emails_build()
        return emails
    except Exception as e:
        print(e)
