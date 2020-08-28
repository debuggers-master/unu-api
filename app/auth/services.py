"""
Authentication logic.
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings  # pylint: disable-msg=E0611
from schemas.users import UserOut, UserIn
from db.db import get_collection, CRUD


###########################################
##             Auth Settings             ##
###########################################

SECRET = settings.SECRET_JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 45

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


###########################################
##            Security Instances         ##
###########################################

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


###########################################
##          Users CRUD Instance          ##
###########################################
users_collection = get_collection("users")
users_crud = CRUD(users_collection)


###########################################
##              Token Schemas            ##
###########################################

class Token(BaseModel):
    """
    Token base schema
    """
    access_token: str = Field(description="The encoded jwt")
    token_type: str = Field(description="The token type: 'Bearer'")


class TokenData(BaseModel):
    """
    Token request schema
    """
    email: Optional[str] = None


###########################################
##          Helper Auth Functions        ##
###########################################

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the enter password with the hashed password stored in db.

    Params:
    ------
    plain_password: str - The plain password from the request form.
    hashed_password: str -The hashed password stored in db.

    Return:
    ------
    Boolean: True if correct password, False if not.
    """

    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    """
    Generate a hash of the current password.

    Params:
    ------
    plain_password: str - The plain password from the request form.

    Return:
    ------
    hashed_password: str - The password hashed.
    """

    return pwd_context.hash(plain_password)


async def authenticate_user(email: str, password: str) -> UserOut:
    """
    Auhenticate the user recived in the request.

    Params:
    ------
    email: str - The user email
    password: str - The password email

    Return:
    ------
    user: UserOut - The user class. If not authenticated, returns False.
    """

    user = await users_crud.find({"email": email})
    if not user:
        return False
    if not verify_password(password, user.get("password")):
        return False
    return UserOut(**user)


def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None) -> bytes:
    """
    Return a encoded jwt.

    Params:
    ------
    data: dict
        The data to encoded in jwt paayload.
    expires_delta: timedelta (optional)
        The time in minutes to expire token.

    Return:
    ------
    encode_jwt: bytes - The encoded json web token.
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


###########################################
##        Authentication Middleware      ##
###########################################

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    """
    Verify the user in token and return the user if token is valid.

    Params:
    ------
    taken: str - The jwt in the header request.

    Return:
    user: UserOut - The user data.
    """
    try:
        payload: dict = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = await users_crud.find({"email": token_data.email})
    if user is None:
        raise credentials_exception
    return UserOut(**user)


###########################################
##             Register Function         ##
###########################################

async def register_user(user: UserIn) -> str:
    """
    Create a new user.

    Params:
    ------
    user: UserIn - The principal user data.

    Return:
    ------
    user: UserOut - The complete user data.
    """

    new_user = user.dict()
    new_user.update({"password": hash_password(user.password)})
    new_user.update({"organizations": []})
    new_user.update({"myEvents": []})
    new_user.update({"collaborations": []})
    new_user.update({"userId": str(uuid4())})

    inserted_id = await users_crud.create(new_user)
    if inserted_id is not None:
        return UserOut(**new_user)
    return False
