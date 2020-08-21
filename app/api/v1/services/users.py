"""
Bussiness logic about user operations.
"""

from uuid import uuid4
from db.db import get_collection, CRUD

# COLLECTIONS
USER_COLLECTION_NAME = "users"

# DB collection instances
users_collection = get_collection(USER_COLLECTION_NAME)


# ------------------ User controller operations ----------------- #
class UserService:
    """
    Operations about users.
    """

    def __init__(self):
        self.crud = CRUD(users_collection)

    async def create_user(self, user_data: dict) -> dict:
        """
        Creare a new user.

        Params:
        ------
        user_data: dict - The user info.

        Return:
        ------
        user_id: dict - The user uuid created.
        """

        inserted_id = await self.crud.create(user_data)
        if not inserted_id:
            return None

        return inserted_id
    
    async def get_user(self, email: str) -> dict:
        """
        Return the user that matches with email

        Params:
        ------
        email: str - The user email

        Return:
        ------
        user: list - The event user
        """
        query = {"email": email}
        user = await self.crud.find(query)
        return user


    async def update_user(self, user_id: str, user_data: dict) -> dict:
        """
        Update the user info.

        Params:
        ------
        user_id: str - The user uuid also called userId.
        user_data: dict - The data to update. Can be all user data or only one field.

        Return:
        ------
        updated: dict {"modifiend_count": int} - The number of modified documents.
        """
        query = {"userId": user_id}
        modified_count = await self.crud.update(query, user_data)
        return {"modified_count": modified_count}

    async def delete_user(self, user_id: str) -> None:
        """
        Delete an existing user.

        Params:
        ------
        user_id: str - The user uuid also called userId.

        Return: None
        """
        query = {"userId": user_id}
        await self.crud.delete(query)

