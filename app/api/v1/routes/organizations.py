"""
Organizations Router - Operations about organizations
"""

from fastapi import APIRouter, HTTPException, Depends

from api.v1.services.organization import OrganizationController
from auth.services import get_current_user
from schemas.general import ModifiedCountUrls
from schemas.users import UserOut
from schemas.organizations import (
    OrganizationIn, OrganizationResponse,
    OrganizationDelete, OrganizationUpdate, OrganizationGet)


###########################################
##            Router Instance            ##
###########################################

router = APIRouter()


###########################################
##    Organization Service Instance      ##
###########################################

OrganizationMethods = OrganizationController()


############################################
##      Organization API Endpoints        ##
############################################

@router.post(
    "",
    status_code=201,
    response_model=OrganizationResponse,
    responses={"409": {}, "500": {}})
async def create_organization(
        body: OrganizationIn,
        current_user: UserOut = Depends(get_current_user)):
    """
    Create new organization with **OrganizationIn** Model
    """
    org = await OrganizationMethods.add_organization(
        user_id=current_user.userId,
        organization_data=body.organizationData.dict())

    if org == 409:
        raise HTTPException(status_code=409, detail="Organization name used")
    if org == 500:
        raise HTTPException(status_code=500, detail="Server error")
    return org


@router.put(
    "",
    status_code=200,
    response_model=ModifiedCountUrls,
    responses={"409": {}})
async def update_organization(
        organization: OrganizationUpdate,
        current_user: UserOut = Depends(get_current_user)):
    """
    Update  organization
    """
    modified_count = await OrganizationMethods.update_organization(
        user_id=current_user.userId,
        organization_id=organization.organizationData.organizationId,
        organization_data=organization.organizationData.dict())

    if modified_count is False:
        raise HTTPException(
            status_code=409,
            detail="The organization name is already used")

    return modified_count


@router.delete(
    "", status_code=204,
    responses={"403": {}})
async def delete_organization(
        organization: OrganizationDelete,
        current_user: UserOut = Depends(get_current_user)):
    """
    Delete and organization
    """
    res = await OrganizationMethods.delete_organization(
        user_id=current_user.userId,
        organization_id=organization.organizationId)

    if res == 403:
        raise HTTPException(status_code=403, detail="Forbbiden")


@router.get(
    "",
    status_code=200,
    response_model=OrganizationGet)
async def get_organization(
        organizationId: str,
        current_user: UserOut = Depends(get_current_user)):
    """
    Get an organization
    """
    organization = await OrganizationMethods.get_organization(
        organization_id=organizationId)

    if organization is not None:
        return OrganizationGet(**organization)
    raise HTTPException(status_code=404, detail="Not organizationId Found")
