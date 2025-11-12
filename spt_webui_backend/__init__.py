import fastapi
import sentry_sdk
from contextlib import asynccontextmanager
from fastapi import APIRouter
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import spt_webui_backend.database
import spt_webui_backend.database.migrate
from spt_webui_backend import oauth2, spotify, security, schemas
from spt_webui_backend import routes
from spt_webui_backend.database import crud
from spt_webui_backend.environment import ENVIRONMENT
from spt_webui_backend.schemas import AccessToken

# initialize sentry
if ENVIRONMENT.sentry_dsn:
    sentry_sdk.init(
        dsn=ENVIRONMENT.sentry_dsn,
        traces_sample_rate=1.0,
    )

middleware = [
    Middleware(
        SessionMiddleware,
        secret_key=ENVIRONMENT.secret_key,
        session_cookie="spt-webui-session"
    ),
    Middleware(
        CORSMiddleware,
        allow_methods=["*"],
        allow_headers=["*"], allow_credentials=True,
        allow_origins=[ENVIRONMENT.allowed_origin]
    )
]


@asynccontextmanager
async def lifespan(_app: fastapi.FastAPI):
    # startup stuff
    spt_webui_backend.database.migrate.migrate_to_head()
    yield


app = fastapi.FastAPI(middleware=middleware, lifespan=lifespan)
router = APIRouter()
router.include_router(routes.auth.router)
router.include_router(routes.playback.router)

app.include_router(router, prefix=ENVIRONMENT.api_prefix)
