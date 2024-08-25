import sqlalchemy as sa
import sqlalchemy.orm

import spt_webui_backend.database.models as models
from spt_webui_backend.environment import ENVIRONMENT

engine = sa.create_engine(
    f"mariadb+pymysql://{ENVIRONMENT.database_user}:{ENVIRONMENT.database_password}@localhost/spt_webui",
    pool_recycle=3600
)

SessionLocal = sa.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
