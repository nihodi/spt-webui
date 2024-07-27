import datetime

from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    refresh_token: str

    expires_at: datetime.datetime


class SpotifyUser(BaseModel):
    id: str
