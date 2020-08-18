"""
Users services code
"""
from werkzeug.security import generate_password_hash

from app.db.users import create_user
from app.schemas.users import UserIn, UserInDB

def create_user_in_db(new_user: UserIn):
    """
    Function to hash password and save user in
    in DB using UserInDB model
    """
    hashed_password = generate_password_hash(new_user.password)
    user_in_db = UserInDB(**new_user.dict(), hashed_password=hashed_password)
    create_user(user_in_db)
    return user_in_db
