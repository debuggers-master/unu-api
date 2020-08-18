"""
DB users - Db functions about users
"""

from bson.json_util import ObjectId
from .db import get_collection, jsonify

# Users collection
db = get_collection('users')


# ------------------- Useful functions ------------------ #
def create_query(email: str = None, user_id: str = None) -> dict:
    """
    Return a dict with the correct query acording to the passed data

    Params:
    ------
    email: str (Optional)
        The user email.
    user_id: str (Optional)
        The user id.

    Return:
    ------
    query: dict
        The correct mongo query.
    """

    query = {"email": email}
    if user_id is not None:
        query = {"_id": ObjectId(user_id)}

    return query


# -------------------- Users methods -------------------- #

async def get_user(email: str = None, user_id: str = None) -> dict:
    """
    Return the users that matches with the email passed.

    Params:
    ------
    email: str (Optional)
        The user email.
    user_id: str (Optional)
        The user id.

    Return:
    ------
    user: dict
        The user data.
    """

    query = create_query(email, user_id)
    user = await db.find_one(query)
    return jsonify(user)


async def create_user(user_data: dict) -> str:
    """
    Insert a new user to collection

    Params:
    ------
    user_data: dict
        The user data.

    Return:
    ------
    inserted_id: str
        The user inserted id.
    """

    user = await db.insert_one(user_data)
    return str(user.inserted_id)


async def update_user(
        user_data: dict,
        email: str = None,
        user_id: str = None
) -> str:
    """
    Update an existing user in collection.

    Params:
    ------
    user_data: dict
        The user data.
          Params:
    email: str (Optional)
        The user email.
    user_id: str (Optional)
        The user id.

    Return:
    ------
    modified_count: str
        The modified documents count (always str(1))
    """

    query = create_query(email, user_id)
    operation = {"$set": user_data}
    updated_user = await db.update_one(query, operation)
    return str(updated_user.modified_count)


async def delete_user(
        email: str = None,
        user_id: str = None
) -> bool:
    """
    Delete an existing user from collection.

    Params:
    ------
    email: str (Optional)
        The user email.
    user_id: str (Optional)
        The user id.

    Return:
    ------
    deleted: Bool
        Return True if the operation is successfull, False if not.
    """

    query = create_query(email, user_id)
    await db.delete_one(query)
    return True


async def add_organization(
        organization_data: dict,
        email: str = None,
        user_id: str = None,
) -> str:
    """
    Add a new organization to the organizations user list

    Params:
    ------
    organization_data: dict
        The organization data.
    email: str (Optional)
        The user email.
    user_id: str (Optional)
        The user id.

    Return:
    ------
    modified_count: str
        The modified documents count (always str(1))
    """

    query = create_query(email, user_id)
    operation = {"$addToSet": {"organizations": organization_data}}
    updated_user = await db.update_one(query, operation)
    return str(updated_user.modified_count)


async def add_collaboration(
        collaboration_data: dict,
        email: str = None,
        user_id: str = None,
) -> str:
    """
    Add a new organization to the collaborations user list

    Params:
    ------
    organization_data: dict
        The organization data.
    email: str (Optional)
        The user email.
    user_id: str (Optional)
        The user id.

    Return:
    ------
    modified_count: str
        The modified documents count (always str(1))
    """

    query = create_query(email, user_id)
    operation = {"$addToSet": {"collaborations": collaboration_data}}
    updated_user = await db.update_one(query, operation)
    return str(updated_user.modified_count)
