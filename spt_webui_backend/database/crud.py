from typing import Optional

from sqlalchemy.orm import Session

from spt_webui_backend.database import models


def create_user(db: Session, user: models.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_discord_id(db: Session, discord_id: int) -> Optional[models.User]:
    return db.query(models.User).where(models.User.id == discord_id).first()


def create_user_if_not_exists(db: Session, user: models.User):
    existing_user = db.query(models.User).where(models.User.discord_user_id == user.discord_user_id).first()

    # todo: update user's discord_display_name
    if existing_user:
        return existing_user

    return create_user(db, user)