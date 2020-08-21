"""
User Router - Operations about users
"""
from fastapi import APIRouter, HTTPException


from schemas.organizations import OrganizationIn, OrganizationOut
from api.v1.services.organization import OrganizationController

# Router instance
router = APIRouter()


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