"""
Events Router - Operations about events
"""

from fastapi import APIRouter, HTTPException

from schemas.events import InformationIn, InformationDB

# Router instance
router = APIRouter()
