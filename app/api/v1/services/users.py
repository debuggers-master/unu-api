"""
Bussiness login about user operations.
"""

from uuid import uuid4
from db.db import get_collection, CRUD

# COLLECTIONS
USER_COLLECTION_NAME = "users"
ORGANIZATIONS_COLLECTION_NAME = "organizations"
EVENTS_COLLECTION_NAME = "events"


# DB collection instances
users_collection = get_collection(USER_COLLECTION_NAME)
users_crud = CRUD(users_collection)

organizations_collection = get_collection(ORGANIZATIONS_COLLECTION_NAME)
organizations_crud = CRUD(organizations_collection)

events_collection = get_collection(EVENTS_COLLECTION_NAME)
events_crud = CRUD(events_collection)


# ------------------ User controller operations ----------------- #

async def update_user(user_id: str, user_data: dict) -> dict:
    """
    Update the user info.

    Params:
    ------
    user_id: str
        The user uuid also called userId.
    user_data: dict
        The data to update. Can be all user data or only one field.

    Return:
    ------
    updated: dict {"modifiend_count": int}
        A dict with the number of modified documents.
    """

    query = {"userId": user_id}
    modified_count = await users_crud.update(query, user_data)
    return {"modified_count": modified_count}


async def delete_user(user_id: str) -> None:
    """
    Delete an existing user.

    Params:
    ------
    user_id: str
        The user uuid also called userId.

    Return:
    ------
    None
    """

    query = {"userId": user_id}
    await users_crud.delete(query)


async def add_organization(user_id: str, organization_data: dict) -> dict:
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
    organizationId: str
        The organization uuid unique identifier.
    """

    organization_id = str(uuid4())
    organization_data.update({"organizationId": organization_id})

    # Create a new organization
    inserted_id = organizations_crud.create(organization_data)
    if not inserted_id:
        return False
    # Add the organization info to the user.
    modified_count = await users_crud.add_to_set(
        query={"userId": user_id},
        array_name="organizations",
        data={"organizationId": organization_id,
              "name": organization_data.get("name")})
    if not modified_count:
        return False
    return {"organizationId": organization_id}


async def update_organization(
        user_id: str, organization_id: str, organization_data: dict) -> dict:
    """
    Update a existing organization.

    Params:
    ------
    user_id: str
        The user id.
    organization_id: str
        The organization id.
    organization_data: dict
        The organization data.

    Return:
    ------
    organizationId: str
        The organization uuid unique identifier.
    """

    # Update in the collection
    query_orga = {"organizationId": organization_id}
    modified_count = organizations_crud.update(query_orga, organization_data)
    if not modified_count:
        return False

    # Update in the user list
    query_user = {"userId": user_id}
    organizations_list = await users_crud.find(query_user, filters=["organizations"])
    try:
        # Get the desired organization
        organization = [
            org for org in organizations_list if org.organizationId == organization_id]
        index = organizations_list.index(organization[0])
        organization_data.update(
            {"organizationId": organization[0].get("organizationId")})

        # Update the data
        organizations_list[index] = organization_data
    except KeyError:
        # The organization is not in the list.
        return False

    modified_count = await users_crud.add_to_set(
        query_user, "organizations", organizations_list)
    if not modified_count:
        return False
    return {"modifed_count": modified_count}


async def delete_organization(user_id: str, organization_id: str) -> None:
    """
    Delete an existing organization.

    Params:
    ------
    user_id: str
        The user id.
    organization_id: str
        The organization id.

    Return:
    ------
    None
    """

    await organizations_collection.delete({"organizationId": organization_id})
    query = {"userId": user_id}
    modified_count = await users_crud.pull_array(
        query=query,
        array_name="organizations",
        condition={"organizationId": organization_id})

    if modified_count:
        await events_crud.delete_many({"organizationId": organization_id})
