"""
Authorization endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611

from db.users import get_user
from schemas.users import UserOut, UserIn
from .services import (
    authenticate_user,
    credentials_exception,
    create_access_token,
    Token,
    register_user)

# Router instance
auth_router = APIRouter()


# Login Request
class LoginRequest(BaseModel):
    """
    Login request schema.
    """
    email: str = Field(...,
                       description="User email",
                       example="emanuel@gmail.com")
    password: str = Field(...,
                          description="The user password",
                          example="the_awos0me_secr3t")


class AuthResponse(Token):
    """
    Login Response schema.
    """
    user: UserOut


# -------------------- Auth router ------------------------- #

@auth_router.post("/login", response_model=AuthResponse)
async def login_for_acces_token(login_data: LoginRequest):
    """
    Verify the user credentials and return a jwt.
    """
    user = await authenticate_user(login_data.email, login_data.password)
    if not user:
        raise credentials_exception
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "Bearer", "user": user}


@auth_router.post("/signup", response_model=AuthResponse)
async def signup(user: UserIn):
    """
    Register a new user and login the user.
    """
    existing_user = await get_user(email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The email already exists"
        )

    # Only make register if the user is new.
    new_user = await register_user(user)
    if not new_user:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "Bearer", "user": new_user}
