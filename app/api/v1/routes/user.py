"""
User Router - Operations about users
"""
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Depends

from schemas.organizations import OrganizationIn, OrganizationOut, OrganizationDB
from schemas.events import EventIn, EventOut, EventDelete
from db.users import add_organization
from db.events import create_event, delete_event
from auth.services import get_current_user

# Router instance
router = APIRouter()


@router.post("/organizations/", status_code=201, response_model=OrganizationOut)
async def create_organization(organization: OrganizationIn):
    """
    Create new organization with **OrganizationIn** Model
    """
    new_org = OrganizationDB(**organization.dict())
    new_org.organization_id = str(uuid4())
    new_org = new_org.dict()
    modified = await add_organization(organization_data=new_org, email=organization.ownerEmail)

    if int(modified) < 1:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return OrganizationOut(**new_org)

@router.post("/event/", status_code=201, response_model=EventOut)
async def create_new_event(event: EventIn):
    """
    Create new event with **EventIn** Model
    """
    new_event = event.dict()
    new_event.update({"event_id": str(uuid4())})

    inserted_id = await create_event(event_data=event)
    if inserted_id is not None:
        return EventOut(**new_event)
    raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/event/", status_code=204)
async def delete_created_event(event: EventDelete):
    """
    Create new event with **Event** Model
    """
    delete_act = await delete_event(event_id=event.event_id)
    print(delete_act)
    if delete_act is True:
        pass
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")
