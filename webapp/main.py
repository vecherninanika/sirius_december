from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from fastapi_pagination import add_pagination

from webapp.api.auth.router import auth_router
from webapp.api.ingredient.router import ingredient_router
from webapp.api.recipe.router import recipe_router
from webapp.metrics import metrics
from webapp.on_shutdown import stop_producer
from webapp.on_startup.kafka import create_producer
from webapp.on_startup.redis import start_redis
from webapp.middleware.logger import LogServerMiddleware
from webapp.middleware.metrics import MeasureLatencyMiddleware


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(LogServerMiddleware)
    app.add_middleware(MeasureLatencyMiddleware)

    # CORS Middleware should be the last.
    # See https://github.com/tiangolo/fastapi/issues/1663 .
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def setup_routers(app: FastAPI) -> None:
    app.add_route('/metrics', metrics)

    app.include_router(auth_router)
    app.include_router(ingredient_router)
    app.include_router(recipe_router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await start_redis()
    await create_producer()
    print('START APP')
    yield
    await stop_producer()
    print('END APP')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)

    setup_middleware(app)
    setup_routers(app)
    # add_pagination(app)

    return app
