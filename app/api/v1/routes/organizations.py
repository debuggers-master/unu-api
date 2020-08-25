# """
# Organizations Router - Operations about organizations
# """

from fastapi import APIRouter, HTTPException

from schemas.organizations import OrganizationIn, OrganizationOut, OrganizationDelete, OrganizationUpdate
from api.v1.services.organization import OrganizationController

# Router instance
router = APIRouter()

#Organizations service to DB fuctions
OrgMethos = OrganizationController()

@router.post("",
             status_code=201,
             response_model=OrganizationOut)
async def create_organization(organization: OrganizationIn):
    """
    Create new organization with **OrganizationIn** Model
    """
    org = await OrgMethos.add_organization(
        user_id=organization.userId,
        organization_data=organization.organizationData.dict())

    org_out = OrganizationOut(**organization.organizationData.dict(), **org)
    if org_out.organizationId is None:
        raise HTTPException(status_code=409, **org)
    return org_out

@router.put("",
             status_code=200)
async def update_organization(organization: OrganizationUpdate):
    """
    Update  organization
    """

    modified_count = await OrgMethos.update_organization(
                                user_id=organization.userId,
                                organization_id=organization.organizationData.organizationId,
                                organization_data=organization.organizationData.dict())
    return modified_count

@router.delete("",
               status_code=204)
async def delete_organization(organization: OrganizationDelete):
    """
    Delete and organization
    """
    await OrgMethos.delete_organization(
        user_id=organization.userId,
        organization_id=organization.organizationId)


# @router.get("",
#             status_code=200,
#             response_model=OrganizationOut)
# async def get_organization(organizationId:str):
#     """
#     Get a organization using organizationId
#     """
#     org_info = await OrgMethos.get_organization(
#         organization_id=organizationId)

#     return OrganizationOut(**org_info)


# @router.put("",
#             status_code=204,
#             )
# async def update_organization(organization: OrganizationUpdate):
#     """
#     Edit a Organization name and/or description
#     """
#     await OrgMethos.update_organization(
#         user_id=organization.userIdOwner,
#         organization_id=organization.organizationId,
#         organization_data=organization.dict())




# @router.delete("",
#                status_code=204)
# async def delete_organization(organization: OrganizationDelete):
#     """
#     Delete a organization  with **OrganizationDelete** Model
#     """
#     await OrgMethos.delete_organization(
#         user_id=organization.userIdOwner,
#         organization_id=organization.organizationId)
