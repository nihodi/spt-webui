from typing import Optional, List

from pydantic_settings import BaseSettings, JsonConfigSettingsSource, PydanticBaseSettingsSource
from pydantic import Field


class CliArgs(BaseSettings):
    env_files: List[str] = Field(validation_alias="env-file", default=[".env"], description="List of environment files to load")

    class Config:
        cli_parse_args = True


CLI_ARGS: CliArgs = CliArgs()

class Environment(BaseSettings):
    spotify_client_id: str
    spotify_client_secret: str

    spotify_redirect_uri: str = "http://localhost:8000/auth/callback"

    spotify_allowed_account_id: str

    spotify_playlist_id: Optional[str] = None

    database_user: str
    database_password: str

    discord_client_id: str
    discord_client_secret: str

    discord_redirect_uri: str = "http://localhost:8000/auth/callback/discord"
    discord_webhook_url: Optional[str] = None

    secret_key: str

    frontend_url: str = "http://localhost:4200"

    allowed_origin: str = "http://localhost:4200"

    api_prefix: str = ""
    port: int = 8000

    token_save_location: str = "saved_token"

    sentry_dsn: Optional[str] = None

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # use json file as last priority settings source
        return init_settings, env_settings, dotenv_settings, file_secret_settings, JsonConfigSettingsSource(settings_cls)

    class Config:
        env_file = CLI_ARGS.env_files
        json_file = "/etc/spt-webui/settings.json" # TODO: make a CLI parameter?

ENVIRONMENT: Environment = Environment()
