from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from httpx import HTTPStatusError

from wordle_leaderboard.api.schemas import Messages
from wordle_leaderboard.clients.google import GoogleClient
from wordle_leaderboard.clients.google import GoogleCredentialsError
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
        emails = await google_client.get_emails(queries=["from:aaron00brogan@gmail.com"])
        emails = Messages(**emails)
        emails = [await google_client.get_emails(email_id=message.id) for message in emails.messages]
        return emails
    except HTTPStatusError:
        return PlainTextResponse(
            str("Error retrieving Emails from google."), status_code=400
        )


@router.get("/authenticate", operation_id="authenticate")
async def handle_authenticate(
    google_client: GoogleClient = Depends(get_google_client),
):
    try:
        google_client.credentials()
    except GoogleCredentialsError as exc:
        return PlainTextResponse(str(exc), status_code=401)
    return "OK"
