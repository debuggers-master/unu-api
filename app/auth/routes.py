"""
Authorization endpoints.
"""

from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611

from mails.service import send_welcome_email
from schemas.users import UserOut, UserIn

from .services import (
    authenticate_user, credentials_exception,
    create_access_token, Token, register_user, users_crud)


###########################################
##             Router Instance           ##
###########################################

auth_router = APIRouter()


###########################################
##      Request and Response Models      ##
###########################################

class LoginRequest(BaseModel):
    """
    Login request schema.
    """
    email: str = Field(
        ...,
        description="user email",
        example="stan_lee@marvel.com"
    )
    password: str = Field(
        ...,
        description="user password",
        example="with_great_power_comes_great_responsibility"
    )


class AuthResponse(Token):
    """
    Login Response schema.
    """
    user: UserOut


###########################################
##               Auth Router             ##
###########################################

@auth_router.post(
    "/login",
    status_code=200,
    response_model=AuthResponse)
async def login_for_acces_token(body: LoginRequest):
    """
    Verify the user credentials and return jwt and user info.
    """
    user = await authenticate_user(body.email, body.password)
    if not user:
        raise credentials_exception

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "Bearer", "user": user}


@auth_router.post("/signup",
                  status_code=201,
                  response_model=AuthResponse)
async def signup(user: UserIn, backgroud_task: BackgroundTasks):
    """
    Register a new user and login the user.
    """
    existing_user = await users_crud.find({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The email already exists")

    # Only make register if the user is new.
    new_user = await register_user(user)
    if not new_user:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Send welcome email in background
    backgroud_task.add_task(send_welcome_email, user.firstName, user.email)

    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token,
            "token_type": "Bearer", "user": new_user}
