"""
Main app entry point.
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1 import api_router
from auth.routes import auth_router
from config import settings  # pylint: disable-msg=E0611

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

###########################################
##               Middlewares             ##
###########################################

if settings.CORS_ORIGIN:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

###########################################
##                 Routers               ##
###########################################

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(api_router, prefix=settings.API_V1_STR)
