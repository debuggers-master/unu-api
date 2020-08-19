"""
Events Router - Operations about events
"""

from fastapi import APIRouter, HTTPException

from schemas.events import InformationIn, InformationDB
from db.events import update_event



# Router instance
router = APIRouter()


@router.post("/information/", status_code=204)
async def add_information(info: InformationIn):
    """
    Create a dict into events called information
    with **Information** Model
    """
    modified = await update_event(event_id=info.event_id, event_data=InformationDB(**info.dict()))
    if int(modified) < 1:
        raise HTTPException(status_code=500, detail="Internal Server Error")
