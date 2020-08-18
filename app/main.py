"""
Main app entry point.
"""
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.v1 import api_router
from config import settings

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Setting all cors enable origins
if settings.CORS_ORIGIN:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.CORS_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Routers
app.include_router(api_router, prefix=settings.API_V1_STR)
