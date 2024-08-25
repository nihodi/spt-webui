import alembic.config
import alembic.migration
import alembic.command

from spt_webui_backend.database import engine
from spt_webui_backend.database import models


def migrate_to_head() -> None:
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