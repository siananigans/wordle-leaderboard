from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        return Response("Internal server error", status_code=500)
