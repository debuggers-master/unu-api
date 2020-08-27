"""
Bussines logic about organizations.
"""

from uuid import uuid4

from fastapi import BackgroundTasks

from storage.service import upload_file
from db.db import get_collection, CRUD

from .utils import update_image

###########################################
##          Collection Instances         ##
###########################################
USER_COLLECTION_NAME = "users"
users_collection = get_collection(USER_COLLECTION_NAME)

ORGANIZATIONS_COLLECTION_NAME = "organizations"
organizations_collection = get_collection(ORGANIZATIONS_COLLECTION_NAME)

EVENTS_COLLECTION_NAME = "events"
events_collection = get_collection(EVENTS_COLLECTION_NAME)


###########################################
##      Organization Service Class       ##
###########################################

class OrganizationController:
    """
    Opeartions about organizations.
    """

    def __init__(self) -> None:
        """
        Crud instances of the collections needed.
        """
        self.crud = CRUD(organizations_collection)
        self.users = CRUD(users_collection)
        self.events = CRUD(events_collection)
        self.backgroud_task = BackgroundTasks()

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

    async def add_organization(
            self, user_id: str, organization_data: dict) -> dict:
        """
        Add a new organization to the organizations user list
        and in organizations document

        Params:
        ------
        user_id: str - The user id.
        organization_data: dict - The organization data.

        Return:
        ------
        organizationId: str - The organization uuid unique identifier.
        """

        # Check if organization name is unique
        query = {"organizationName": organization_data.get("organizationName")}
        org_exists = await self.crud.find(query)
        if org_exists is not None:
            return {"detail": "This Organizations already exists"}

        # Complete all fields
        organization_id = str(uuid4())
        organization_data.update({"organizationId": organization_id})

        organization_url = organization_data.get("organizationName")
        organization_url = organization_url.replace(" ", "-").lower()
        organization_data.update({"organizationUrl": organization_url})

        organization_data.update({"events": []})

        # Image proccessing
        logo = organization_data.get("organizationLogo")
        image_url = await update_image(image=logo)
        organization_data.update({"organizationLogo": image_url})

        # Create a organization document in organizations collections
        inserted_id = await self.crud.create(organization_data)
        if not inserted_id:
            return {"detail": "Error on saving"}

        # Add the organization info to the user.
        organization_name = organization_data.get("organizationName")
        modified_count = await self.users.add_to_set(
            query={"userId": user_id},
            array_name="organizations",
            data={"organizationId": organization_id,
                  "organizationName": organization_name})

        if not modified_count:
            self.backgroud_task.add_task(
                self.delete_organization, user_id,
                organization_id)
            return {"detail": "User not Found"}

        return {"organizationId": organization_id,
                "organizationLogo": image_url}

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

        query = {"organizationName": organization_data.get("organizationName")}
        org_exists = await self.crud.find(query)
        # Check is organization name is unique
        if org_exists:
            if org_exists.get("organizationId") == organization_id:
                # Create the url name
                organization_url = organization_data.get("organizationName")
                organization_url = organization_url.replace(" ", "-").lower()
                organization_data.update({"organizationUrl": organization_url})
                # Upload Image
                url = ""
                org_logo = organization_data.get("organizationLogo", "")
                if org_logo:
                    if org_logo.startswith("https"):
                        url = org_logo
                    elif org_logo.startswith("data"):
                        url = await upload_file(
                            file_base64=organization_data.get("organizationLogo"))
                        print(url)
                        organization_data.update({"organizationLogo": url})

                # Update in the collection
                query_orga = {"organizationId": organization_id}
                modified_count = await self.crud.update(query_orga, organization_data)
                print(modified_count)
                if not modified_count:
                    return {"modifiedCount": modified_count,
                            "url": {"organizationLogo": url}}
                # Update in the user list
                query = {"userId": user_id,
                         "organizations.organizationId": organization_id}
                data = {"organizations.$": {"organizationId": organization_id,
                                            "organizationName": organization_data.get("organizationName")}}
                modified_count = await self.users.update(query, data)

                return {"modifiedCount": modified_count,
                        "url": {"organizationLogo": url}}
            return False

        # Create the url name
        organization_url = organization_data.get("organizationName")
        organization_url = organization_url.replace(" ", "-").lower()
        organization_data.update({"organizationUrl": organization_url})
        # Upload Image
        url = ""
        org_logo = organization_data.get("organizationLogo", "")
        if org_logo:
            if org_logo.startswith("https"):
                url = org_logo
            elif org_logo.startswith("data"):
                url = await upload_file(
                    file_base64=organization_data.get("organizationLogo"))
                print(url)
                organization_data.update({"organizationLogo": url})

        # Update in the collection
        query_orga = {"organizationId": organization_id}
        modified_count = await self.crud.update(query_orga, organization_data)
        if not modified_count:
            return False
        # Update in the user list
        query = {"userId": user_id,
                 "organizations.organizationId": organization_id}
        data = {"organizations.$": {"organizationId": organization_id,
                                    "organizationName": organization_data.get("organizationName")}}
        modified_count = await self.users.update(query, data)
        return {"modifiedCount": modified_count,
                "url": {"organizationLogo": url}}

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
