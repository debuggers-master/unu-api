"""
User Router - Operations about users
"""

from fastapi import APIRouter, HTTPException

from schemas.users import UserIn, UserOut # pylint: disable-msg=E0611

# Router instance
router = APIRouter()

@router.post("/signin/",
             status_code=201,
             response_model=UserOut)
async def signin(new_user: UserIn):
    """
    EndPoint to SignIn New user
    """
    if True: ## User successful created
        return UserOut
    elif False: ## Email Already exists
        raise HTTPException(status_code=409, detail="Email already register")
    else: ## Wrong Password Confirm
        raise HTTPException(status_code=400, detail="Password does not match")

@router.post("/login/",
             status_code=201,
             response_model=UserOut)
async def login(user_login: UserIn):
    """
    EndPoint to Login New user
    """
    if True: ## User successful Login
        return UserOut
    elif False: ## Email does not register
        raise HTTPException(status_code=409, detail="Email is not register")
    else: ## Wrong Password
        raise HTTPException(status_code=400, detail="Password does not match")

