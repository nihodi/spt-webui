import alembic.command
import alembic.config
import alembic.migration
import sqlalchemy as sa
import sqlalchemy.orm

from spt_webui_backend.environment import ENVIRONMENT

import spt_webui_backend.database.models as models

engine = sa.create_engine(
    f"mariadb+pymysql://{ENVIRONMENT.database_user}:{ENVIRONMENT.database_password}@localhost/spt_webui",
    pool_recycle=3600
)

SessionLocal = sa.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

alembic_config = alembic.config.Config("alembic.ini")

# check if alembic migrations exist
with engine.begin() as connection:
    context = alembic.migration.MigrationContext.configure(connection)
    print(f"Current database version: {context.get_current_revision()}")

    if context.get_current_revision() is None:
        print(
            "WARN: Database version is non-existent. Assuming first run of spt-webui-backend - creating database tables from scratch")

        models.Base.metadata.create_all(bind=engine)

        # make sure alembic knows what we're doing
        alembic.command.stamp(alembic_config, "head")
    else:
        alembic.command.upgrade(alembic_config, "head")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
