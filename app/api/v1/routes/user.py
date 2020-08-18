"""
User Router - Operations about users
"""
from fastapi import APIRouter, HTTPException


from app.schemas.users import UserIn, UserOut # pylint: disable-msg=E0611
from app.db.users import get_user
from app.api.v1.services.users import create_user_in_db

# Router instance
router = APIRouter()

@router.post("/signin/",
             status_code=201,
             response_model=UserOut)
async def signin(new_user: UserIn):
    """
    EndPoint to SignIn New user
    """
    if get_user(email=new_user.email) is not None:
        if new_user.password == new_user.passwordConfirm:
            user_saved = create_user_in_db(new_user)
            return user_saved
        raise HTTPException(status_code=400, detail="Password does not match")
    raise HTTPException(status_code=409, detail="Email already register")


# @router.post("/login/",
#              status_code=201,
#              response_model=UserOut)
# async def login(user_login: UserIn):
#     """
#     EndPoint to Login New user
#     """
#     # if True: ## User successful Login
#     #     return UserOut
#     # elif False: ## Email does not register
#     #     raise HTTPException(status_code=409, detail="Email is not register")
#     # else: ## Wrong Password
#     #     raise HTTPException(status_code=400, detail="Password does not match")
