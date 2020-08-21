"""
Bussines logic about organizations.
"""

from uuid import uuid4
from db.db import get_collection, CRUD

# COLLECTIONS
USER_COLLECTION_NAME = "users"
ORGANIZATIONS_COLLECTION_NAME = "organizations"
EVENTS_COLLECTION_NAME = "events"


# DB collection instances
users_collection = get_collection(USER_COLLECTION_NAME)
organizations_collection = get_collection(ORGANIZATIONS_COLLECTION_NAME)
events_collection = get_collection(EVENTS_COLLECTION_NAME)


# ------------------ Organization controller operations ----------------- #

class OrganizationController:
    """
    Opeartions about organizations.
    """

    def __init__(self):
        self.crud = CRUD(organizations_collection)
        self.users = CRUD(users_collection)
        self.events = CRUD(events_collection)

    async def get_organization(self, organization_id: str) -> dict:
        """
        Retrieve all organization info.

        Params:
        ------
        organization_id: str - The organization uuid.

        Return:
        ------
        organization: dict - The organization data.
        """
        query = {"organizationId": organization_id}
        organization = await self.crud.find(query)
        return organization

    async def add_organization(self, user_id: str, organization_data: dict) -> dict:
        """
        Add a new organization to the organizations user list
        and also  in organizations document

        Params:
        ------
        user_id: str - The user id.
        organization_data: dict - The organization data.

        Return:
        ------
        organizationId: str - The organization uuid unique identifier.
        """

        query = {"name": organization_data.get("name")}
        org_exists = await self.crud.find(query)

        #Check is organization name is unique
        if org_exists is None:
            organization_id = str(uuid4())
            organization_data.update({"organizationId": organization_id})

            # Create the url name
            organization_name = organization_data.get("name")
            organization_name = organization_name.replace(" ", "-").lower()
            organization_data.update({"organizatonName": organization_name})

            # Create a new organization

            # Add the organization info to the user.
            modified_count = await self.users.add_to_set(
                query={"userId": user_id},
                array_name="organizations",
                data={"organizationId": organization_id,
                      "name": organization_data.get("name")})
            if not modified_count:
                return {"detail": "Error UserId is not valid"}

            # Create a organization document in organizations collections
            inserted_id = await self.crud.create(organization_data)
            if not inserted_id:
                #Se debe borrar el documento de usuario si este error se presenta
                return {"detail": "Error on insert organization document"}
            return {"organizationId": organization_id}

        return {"detail": "This Organizations already exists"}



    async def update_organization(
            self, user_id: str, organization_id: str, organization_data: dict) -> dict:
        """
        Update a existing organization.

        Params:
        ------
        user_id: str - The user id.
        organization_id: str - The organization id.
        organization_data: dict - The organization data.

        Return:
        ------
        organizationId: str - The organization uuid unique identifier.
        """
        # Update in the collection
        query_orga = {"organizationId": organization_id}
        modified_count = await self.crud.update(query_orga, organization_data)
        if not modified_count:
            return False

        # Update in the user list
        query = {"userId": user_id,
                 "organizations.organizationId": organization_id}
        data = {"organizations.$": {"organizationId": organization_id,
                                    "name": organization_data.get("name")}}
        modified_count = await self.users.update(query, data)
        return {"modifiedCount": modified_count}

    async def delete_organization(self, user_id: str, organization_id: str) -> None:
        """
        Delete an existing organization and all events related to it.

        Params:
        ------
        user_id: str - The user id.
        organization_id: str - The organization id.

        Return: None
        """
        await self.crud.delete({"organizationId": organization_id})
        query = {"userId": user_id}
        modified_count = await self.users.pull_array(
            query=query,
            array_name="organizations",
            condition={"organizationId": organization_id})

        if modified_count:
            await self.events.delete_many({"organizationId": organization_id})
