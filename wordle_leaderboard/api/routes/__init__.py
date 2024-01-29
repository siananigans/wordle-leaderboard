from fastapi import APIRouter
from wordle_leaderboard.api.routes.emails import router as emails_router

root_router = APIRouter(tags=["root"])

root_router.include_router(emails_router, prefix="/emails")
