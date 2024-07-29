from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    spotify_client_id: str
    spotify_client_secret: str

    spotify_redirect_uri: str = "http://localhost:8000/auth/callback"

    spotify_allowed_account_id: str

    database_user: str
    database_password: str

    discord_client_id: str
    discord_client_secret: str

    discord_redirect_uri: str = "http://localhost:8000/auth/callback/discord"

    secret_key: str

    class Config:
        env_file = ".env"


ENVIRONMENT: Settings = Settings()
