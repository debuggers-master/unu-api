"""
User Router - Operations about users
"""
from fastapi import APIRouter, HTTPException, Depends  # pylint: disable-msg=E0611

from schemas.general import ModifiedCount
from schemas.users import UserUpdate, UserOut
from api.v1.services.users import UserService  # pylint: disable-msg=E0611
from auth.services import get_current_user


# Router instance
router = APIRouter()

UserMethos = UserService()


@router.put("",
            status_code=200,
            response_model=ModifiedCount)
async def update_user(user: UserUpdate,
                      current_user: UserOut = Depends(get_current_user)):
    """
    Update an User
    """
    modified_count = await UserMethos.update_user(
        user_id=user.userId,
        user_data=user.userData.dict())

    if modified_count is False:
        raise HTTPException(
            status_code=409,
            detail="The email is already used by another user")

    return modified_count


@router.delete("",
               status_code=204)
async def delete_user(userId: str,
                      current_user: UserOut = Depends(get_current_user)):
    """
    Delete an User
    """
    await UserMethos.delete_user(user_id=userId)

    # add Delete Events associated with user
    # add Delete Organizations associated with user
