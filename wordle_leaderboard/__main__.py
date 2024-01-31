"""
This module is called when the package is executed as a module.
"""

import sys
import uvicorn
import click
from fastapi import FastAPI
from wordle_leaderboard.middleware.exception import catch_exceptions_middleware


from wordle_leaderboard.api.routes import root_router
from wordle_leaderboard.settings import Settings, init_settings


@click.command()
@click.option("--reload", is_flag=True)
def main(reload=False):
    settings = Settings()
    app = FastAPI(title=settings.server_name)
    app.include_router(root_router)
    # Add exception handler middleware to prevent server crashes
    app.middleware("http")(catch_exceptions_middleware)
    init_settings(settings)
    uvicorn.run(
        app,
        loop="uvloop",
        host=settings.http_host,
        port=settings.http_port,
        log_level="info",
        reload=reload,
    )


if __name__ == "__main__":
    sys.exit(main())
