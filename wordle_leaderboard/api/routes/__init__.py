from fastapi import APIRouter
from wordle_leaderboard.api.routes.google import router as google_router

root_router = APIRouter(tags=["root"])

root_router.include_router(google_router, prefix="/google")
