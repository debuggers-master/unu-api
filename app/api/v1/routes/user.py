"""
User Router - Operations about users
"""
from fastapi import APIRouter, HTTPException


from schemas.organizations import OrganizationIn, OrganizationOut
from api.v1.services.organization import OrganizationController

# Router instance
router = APIRouter()

