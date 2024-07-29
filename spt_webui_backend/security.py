import fastapi
from sqlalchemy.orm import Session
from starlette.requests import Request

from spt_webui_backend.database import models, crud
import spt_webui_backend.database as database

HTTP_401 = {
    "description": "Unathorized. Log in with the /auth/setup/discord endpoint.",
}

def get_current_user(
        request: Request,
        db: Session = fastapi.Depends(database.get_db)
) -> models.User:

    user_id = request.session.get("user_id")
    if not user_id:
        raise fastapi.HTTPException(401, headers={"WWW-Authenticate": "Bearer"})

    user = crud.get_user_by_id(db, user_id)
    if not user:
        request.session.pop("user_id")
        raise fastapi.HTTPException(401, headers={"WWW-Authenticate": "Bearer"})

    return user
