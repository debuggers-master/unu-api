"""
Api router - Merge all api routes.
"""

from fastapi import APIRouter
from app.api.v1.routes import events, particpants, speakers, user

api_router = APIRouter()

api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(
    particpants.router, prefix="/participants", tags=["participants"])
api_router.include_router(
    speakers.router, prefix="/speakers", tags=["speakers"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
