"""
User Router - Operations about users
"""
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Depends

from schemas.organizations import OrganizationIn, OrganizationOut, OrganizationDB
from schemas.events import EventIn, EventOut, EventDelete
from auth.services import get_current_user

# Router instance
router = APIRouter()


