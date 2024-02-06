from wordle_leaderboard.settings import get_settings
from wordle_leaderboard.api.dependencies import (
    get_google_client,
    get_google_credentials,
    get_http_client,
)
from wordle_leaderboard.api.schemas import Messages, Message, MessagePart
from wordle_leaderboard.clients.google import GoogleClient

SCORES = {"aaron00brogan@gmail.com": 0, "sianlennon109@gmail.com": 0}


def get_email_sender(headers: list):
    for header in headers:
        if header.name == "From":
            email_add = header.value.split()[2]
            return email_add[1:-1]


def get_email_score(wordle: str) -> int:
    wordle_score = wordle.split()[2][0]
    if wordle_score.upper() != "X":
        return 7 - int(wordle_score)
    return -3


def score_message_content(email: Message):
    sender = get_email_sender(email.payload.headers)
    todays_score = get_email_score(email.snippet)
    global SCORES
    current_score = SCORES[sender]
    SCORES[sender] = current_score + todays_score
    score_info = {
        "email": sender,
        "todays_score": todays_score,
        "total_score": SCORES[sender],
        "wordle": email.snippet,
    }
    return score_info


async def todays_wordle_results():
    """
    1. Grab wordle emails
    2. Parse emails into scores
    3. Get cached scores
    4. Total up scores
    5. Send total scores to emails
    :return:
    """
    settings = get_settings()
    creds = get_google_credentials(settings)
    http_client = get_http_client()
    async for client in http_client:
        google_client = get_google_client(
            settings=settings, creds=creds, http_client=client
        )
        results = await google_client.get_emails(
            queries=["from:aaron00brogan@gmail.com"]
        )
        emails = Messages(**results)  # Could do this at the end of client function
        todays_scores = []
        for email in emails.messages:
            full_email = await google_client.get_emails(email_id=email.id)
            full_email = Message(**full_email)
            score_info = score_message_content(full_email)
            todays_scores.append(score_info)
