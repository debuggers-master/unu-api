"""
Events Router - Operations about events
"""

from fastapi import APIRouter, HTTPException
from schemas.events import EventIn, EventOut
from schemas.events import InformationIn, InformationDB

# Router instance
router = APIRouter()

@router.get("",
            status_code=200,
            response_model=EventOut)
async def create_event(event: EventIn):
    """
    Get all list of organizations from a user
    """
