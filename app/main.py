"""
Main app entry point.
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1 import api_router
from auth.routes import auth_router
from config import settings  # pylint: disable-msg=E0611

###########################################
##                Metadata               ##
###########################################

tags_metadata = [
    {
        "name": "Auth",
        "description": "Authentication module, include login and sign up endpoints",
    },
    {
        "name": "Users",
        "description": "User Module, allowed methods are get, put and delete users",
    },
    {
        "name": "Organizations",
        "description": "Organizations Module, allowed methods are get, put, post and delete organizations information",
    },
    {
        "name": "Events",
        "description": "Events Module, allowed methods are get, put, post and delete events information",
    },
    {
        "name": "Participants",
        "description": "Participants Module, allowed methods are get, put, post and delete events Participants",
    },
    {
        "name": "Mails",
        "description": "Mails Module, allowe method is post events information",
    }
]


app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="An awesome app to create and manage your events ",
    version="1.0",
    openapi_tags=tags_metadata
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
