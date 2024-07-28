import sqlalchemy as sa
import sqlalchemy.orm

BaseModel = sa.orm.DeclarativeBase


class Base(BaseModel):
    pass


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)

    discord_user_id = sa.Column(sa.BigInteger, unique=True)
    discord_display_name = sa.Column(sa.Unicode(255))
