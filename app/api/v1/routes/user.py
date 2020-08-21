"""
User Router - Operations about users
"""
from fastapi import APIRouter, HTTPException

<<<<<<< HEAD
from schemas.organizations import OrganizationIn, OrganizationOut, OrganizationDB
from schemas.events import EventIn, EventOut, EventDelete
from auth.services import get_current_user
=======

from schemas.organizations import OrganizationIn, OrganizationOut
from schemas.events import EventIn, EventOut
from api.v1.services.organization import OrganizationController
>>>>>>> 2806347c41b9bfcf72ffba2820a2eb6c03721b6c

# Router instance
router = APIRouter()


<<<<<<< HEAD
=======
#Organizations service to DB fuctions
OrgMethos = OrganizationController()

@router.post("/organizations/",
             status_code=201,
             response_model=OrganizationOut)
async def create_organization(organization: OrganizationIn):
    """
    Create new organization with **OrganizationIn** Model
    """
    org = await OrgMethos.add_organization(user_id=organization.userIdOwner,
                                           organization_data=organization.dict())
    org_out = OrganizationOut(**organization.dict(), **org)
    if org_out.organizationId is None:
        raise HTTPException(status_code=409, **org)
    return org_out


@router.get("organizations/",
            status_code=200, 
            response_model=OrganizationOut)
async def get_organizations(user_id: OrganizationIn):
    """
    Get all list of organizations from a user
    """
    pass



@router.get("event/",
            status_code=200, 
            response_model=EventOut)
async def create_event(event: EventIn):
    """
    Get all list of organizations from a user
    """
    pass
>>>>>>> 2806347c41b9bfcf72ffba2820a2eb6c03721b6c
