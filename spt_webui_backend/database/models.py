import sqlalchemy as sa
import sqlalchemy.orm
from sqlalchemy.orm import Mapped, mapped_column

BaseModel = sa.orm.DeclarativeBase


class Base(BaseModel):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)

    discord_user_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True)
    discord_display_name: Mapped[str] = mapped_column(sa.Unicode(255))
