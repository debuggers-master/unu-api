"""
Events Router - Operations about events
"""

from fastapi import APIRouter
from schemas.events import EventIn, EventBase # pylint: disable-msg=E0611

# Router instance
router = APIRouter()


@router.post("/event/",
             status_code=201,
             response_model=EventBase)
async def event(new_event: EventIn):
    """
    EndPoint to create new event
    """
    if True: ## User successful created
        return UserOut
    elif False: ## Email Already exists
        raise HTTPException(status_code=409, detail="Email already register")
    else: ## Wrong Password Confirm
        raise HTTPException(status_code=400, detail="Password does not match")
