from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.api import api_router
from model import models

from core.config import settings
from db.session import SessionLocal, engine

app = FastAPI()

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

models.Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix=settings.API_V1_STR)

