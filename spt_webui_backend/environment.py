from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    spotify_client_id: str
    spotify_client_secret: str

    spotify_redirect_uri: str = "http://localhost:8000/auth/callback"

    spotify_allowed_account_id: str

    class Config:
        env_file = ".env"


ENVIRONMENT: Settings = Settings()
