"""
User Router - Operations about users
"""
from fastapi import APIRouter, HTTPException, Depends, Query

from auth.services import get_current_user
from schemas.general import ModifiedCount
from schemas.users import UserUpdate, UserOut
from api.v1.services.users import UserService


###########################################
##            Router Instance            ##
###########################################

router = APIRouter()


###########################################
##         User Service Instance         ##
###########################################

UserMethods = UserService()


###########################################
##          Users API Endpoints          ##
###########################################

@router.get(
    "",
    status_code=200,
    response_model=UserOut,
    responses={"404": {}})
async def get_loged_user(current_user: UserOut = Depends(get_current_user)):
    """
    Get user info of loged user.
    """
    user = await UserMethods.get_user(current_user.email)
    return user


@router.put(
    "",
    status_code=200,
    response_model=ModifiedCount,
    responses={"409": {}})
async def update_user(
        user: UserUpdate,
        current_user: UserOut = Depends(get_current_user)):
    """
    Update an User
    """
    modified_count = await UserMethods.update_user(
        user_id=current_user.userId,
        user_data=user.userData.dict())

    if modified_count is False:
        raise HTTPException(
            status_code=409,
            detail="Email alreayd used")

    return modified_count


@router.delete(
    "",
    status_code=204,
    responses={"403": {}})
async def delete_user(
        userId: str = Query(...),
        current_user: UserOut = Depends(get_current_user)):
    """
    Delete an User
    """
    if current_user.userId != userId:
        raise HTTPException(status_code=403, detail="Forbbiden")

    await UserMethods.delete_user(user_id=userId)
