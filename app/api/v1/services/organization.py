"""
Bussines logic about organizations.
"""

from uuid import uuid4
from fastapi import BackgroundTasks

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
            return 409

        # Complete all fields
        organization_id = str(uuid4())
        organization_data.update({"userOwner": user_id})
        organization_data.update({"organizationId": organization_id})

        organization_name = organization_data.get("organizationName")
        organization_url = self.create_url(organization_name)
        organization_data.update({"organizationUrl": organization_url})

        organization_data.update({"events": []})

        # Image proccessing
        logo = organization_data.get("organizationLogo")
        image_url = await update_image(image=logo)
        organization_data.update({"organizationLogo": image_url})

        # Create a organization document in organizations collections
        inserted_id = await self.crud.create(organization_data)
        if not inserted_id:
            return 500

        # Add the organization info into the user.
        modified_count = await self.users.add_to_set(
            query={"userId": user_id},
            array_name="organizations",
            data={"organizationId": organization_id,
                  "organizationName": organization_name})

        if not modified_count:
            await self.delete_organization(user_id, organization_id)
            return {"detail": "User not Found"}

        return {"organizationId": organization_id,
                "organizationLogo": image_url}

    async def update_organization(
            self, user_id: str,
            organization_id: str,
            organization_data: dict
    ) -> dict:
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

        # Check is organization name is unique
        organization_name = organization_data.get("organizationName")
        query = {"organizationName": organization_name}
        org_exists = await self.crud.find(query)

        if org_exists:
            if org_exists["organizationId"] != organization_id:
                return False

        # Get actual data to update relational entities
        query = {"organizationId": organization_id}
        org_exists = await self.crud.find(query)

        # Image proccessing
        logo = organization_data.get("organizationLogo")
        image_url = await update_image(image=logo)
        organization_data.update({"organizationLogo": image_url})

        # Update url
        new_url = self.create_url(organization_name)
        organization_data.update({"organizationUrl": new_url})

        # Update in the collection
        modified_count = await self.crud.update(query, organization_data)
        if not modified_count:
            # The collection is the same
            return {"modifiedCount": modified_count,
                    "url": {"organizationLogo": image_url}}

        # Update in the user list in background
        new_data = {"organizationId": organization_id,
                    "organizationName": organization_data["organizationName"]}
        query = {"userId": user_id,
                 "organizations.organizationId": organization_id}
        data = {"organizations.$": new_data}
        await self.users.update(query, data)

        # Update the sublists myEvents
        query = {"myEvents.organizationName": org_exists["organizationName"]}
        data = {"myEvents.$.organizationName": new_data["organizationName"]}

        # Update the sublists collaborations
        await self.users.update(query, data)
        query = {
            "collaborations.organizationName": org_exists["organizationName"]}
        data = {
            "collaborations.$.organizationName": new_data["organizationName"]}
        await self.users.update(query, data, many=True)

        # Update all events
        org_url = org_exists["organizationUrl"]
        await self.events.update(
            {"organizationUrl": org_url},
            {"organizationName": organization_name, "organizationUrl": new_url})

        return {"modifiedCount": modified_count,
                "url": {"organizationLogo": image_url}}

    async def delete_organization(
            self, user_id: str, organization_id: str) -> None:
        """
        Delete an existing organization and all events related to it.

        Params:
        ------
        user_id: str - The user id.
        organization_id: str - The organization id.
        """
        query = {"organizationId": organization_id}
        org = await self.crud.find(query)

        if not org:
            return None

        if org.get("userOwner") != user_id:
            return 403

        
        events_org = org["events"]

        # Remove organization
        await self.crud.delete(query)

        # Remove from user
        await self.users.pull_array(
            query={"userId": user_id},
            array_name="organizations",
            condition={"organizationId": organization_id})

        # Remove all related events
        query = {"organizationUrl": org["organizationUrl"]}
        await self.events.delete_many(query)
        await self.users.pull_array(
            query={"userId": user_id},
            array_name="events",
            condition={"organizationName": org["organizationName"]},
            many=True)

        #Remove all  my_events Related in users own docs
        for event in events_org:
            print("Deleted Event")
            await self.users.pull_array(
                query={"userId": user_id},
                array_name="myEvents",
                condition={"eventId": event["eventId"]}
            )
        
        # Delete collaborations related events Related in user docs


    def create_url(self, organization_name: str):
        """
        Create a correct url
        """
        organization_url = organization_name.replace(" ", "-").lower()
        return organization_url
