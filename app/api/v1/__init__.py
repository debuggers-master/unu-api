"""
Api router - Merge all api routes.
"""

from fastapi import APIRouter
from api.v1.routes import events, particpants, user, organizations

api_router = APIRouter()

api_router.include_router(events.router,
                          prefix="/events",
                          tags=["Events"])

api_router.include_router(particpants.router,
                          prefix="/participants",
                          tags=["Participants"])

api_router.include_router(user.router,
                          prefix="/users",
                          tags=["Users"])

api_router.include_router(organizations.router,
                          prefix="/organizations",
                          tags=["Organizations"])
