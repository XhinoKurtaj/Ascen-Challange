from fastapi import APIRouter

from api.endpoints import timer_api, email_api, pdf_api

api_router = APIRouter()
api_router.include_router(timer_api.router, prefix="/time", tags=["time"])
api_router.include_router(email_api.router, prefix="/email", tags=["email"])
api_router.include_router(pdf_api.router, prefix="/pdf", tags=["pdf"])
