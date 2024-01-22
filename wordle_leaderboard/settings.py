from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    http_host: str = Field("0.0.0.0")
    http_port: int = Field(8000)
    server_name: str = "wordle-leaderboard"

    google_client_id: str
    google_project_id: str
    google_auth_uri: str
    google_token_uri: str
    google_auth_provider_x509_cert_url: str
    google_client_secret: str
    google_redirect_uris: list[str]

    google_base_url: str


# will be initialized on startup
_settings = None


def init_settings(settings: Settings):
    global _settings
    if _settings is not None:
        raise RuntimeError("settings already initialized")
    # kwargs override environment variables
    _settings = settings


def get_settings():
    if _settings is None:
        raise RuntimeError("settings not initialized")
    return _settings
