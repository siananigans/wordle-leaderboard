"""
This module is called when the package is executed as a module.
"""

import sys
import uvicorn
import click
from fastapi import FastAPI

from wordle_leaderboard.settings import Settings


@click.command()
@click.option("--reload", is_flag=True)
def main(reload=False):
    settings = Settings()
    app = FastAPI(title=settings.server_name)
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
