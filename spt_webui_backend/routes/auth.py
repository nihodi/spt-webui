import datetime
import fastapi
import requests_oauthlib
import urllib.parse
from fastapi import APIRouter, Request
from typing import Optional

from spt_webui_backend import oauth2, spotify, database, schemas, security
from spt_webui_backend.database import crud
from spt_webui_backend.schemas import AccessToken
from spt_webui_backend.environment import ENVIRONMENT

router = APIRouter(tags=["auth"])

@router.get("/auth/callback")
def spotify_auth_callback(
        code: Optional[str] = None,
        error: Optional[str] = None,
):
    if code is None:
        raise fastapi.HTTPException(status_code=401, detail=error)

    session = requests_oauthlib.OAuth2Session(
        ENVIRONMENT.spotify_client_id,
        redirect_uri=ENVIRONMENT.spotify_redirect_uri,
    )

    token = session.fetch_token(
        "https://accounts.spotify.com/api/token",
        code,
        client_secret=ENVIRONMENT.spotify_client_secret,
    )

    expires = datetime.datetime.now() + datetime.timedelta(seconds=token["expires_in"])
    token = AccessToken(access_token=token["access_token"], refresh_token=token["refresh_token"], expires_at=expires)

    session = oauth2.get_oauth_session(token)
    tmp_spotify = spotify.Spotify(session)
    user = tmp_spotify.get_me()

    if user.id != ENVIRONMENT.spotify_allowed_account_id:
        raise fastapi.HTTPException(status_code=401, detail="You are not allowed here ;)")

    oauth2.set_current_token(token)


@router.get("/auth/setup")
def spotify_auth_setup():
    return fastapi.responses.RedirectResponse("https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "client_id": ENVIRONMENT.spotify_client_id,
        "response_type": "code",
        "redirect_uri": ENVIRONMENT.spotify_redirect_uri,
        "scope": oauth2.SPOTIFY_SCOPES,
    }))


@router.get("/auth/setup/discord", status_code=fastapi.status.HTTP_307_TEMPORARY_REDIRECT)
def discord_login_redirect():
    return fastapi.responses.RedirectResponse("https://discord.com/oauth2/authorize?" + urllib.parse.urlencode({
        "client_id": ENVIRONMENT.discord_client_id,
        "response_type": "code",
        "redirect_uri": ENVIRONMENT.discord_redirect_uri,
        "scope": "identify",
        "prompt": "none"
    }))


@router.get("/auth/callback/discord")
def discord_auth_callback(
        request: Request,
        code: Optional[str] = None,
        error: Optional[str] = None,
):
    if code is None:
        raise fastapi.HTTPException(status_code=401, detail=error)

    session = requests_oauthlib.OAuth2Session(
        ENVIRONMENT.discord_client_id,
        redirect_uri=ENVIRONMENT.discord_redirect_uri,
        scope="identify",
    )

    session.fetch_token(
        "https://discord.com/api/oauth2/token",
        code=code,
        client_secret=ENVIRONMENT.discord_client_secret
    )

    resp = session.get("https://discord.com/api/v10/users/@me")
    resp.raise_for_status()

    discord_user = resp.json()
    # get their display name, and if it is not set, get their username
    discord_id = int(discord_user["id"])
    username = discord_user.get("global_name") or discord_user["username"]

    with database.SessionLocal() as db:
        user = database.models.User(discord_user_id=discord_id, discord_display_name=username)
        user = crud.create_user_if_not_exists(db, user)

    request.session["user_id"] = user.id

    # todo: make this an env variable
    return fastapi.responses.RedirectResponse(ENVIRONMENT.frontend_url)

@router.get(
    "/users/me",
    responses={
        200: {
            "model": schemas.User
        },
        401: security.HTTP_401
    }

)
def get_current_user(
        user: database.models.User = fastapi.Depends(security.get_current_user)
):
    return user


@router.post("/logout")
def logout(
        request: Request
):
    request.session.clear()
