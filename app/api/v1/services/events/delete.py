"""
Bussines Logic for update events elemets.
"""

from db.db import get_collection, CRUD
from .utils import _make_query, events_crud


###########################################
##          Collection Instances         ##
###########################################

participants_collection = get_collection("participants")
users_collection = get_collection("users")
organizations_collection = get_collection("organizations")


###########################################
##        Events - Delete Service        ##
###########################################

class DeleteEvent:
    """
    Methods for delete event elemnts.
    """

    def __init__(self):
        self.crud = events_crud
        self.users = CRUD(users_collection)
        self.participants = CRUD(participants_collection)
        self.organizations = CRUD(organizations_collection)

    async def all(self, event_id: str, email: str) -> dict:
        """
        Dellete all event info.

        Params:
        ------
        event_id: str - The uuid of the target event.

        Return:
        ------
        {deleted: bool} - True if deleted, False if nothig happens.
        """
        query = _make_query(event_id)
        event = await self.crud.find(query)
        # Keep the proccess only if the event exist.
        if not event:
            return None

        # Delete event
        deleted_count = await self.crud.delete(query)
        # Delete the participants collection
        await self.participants.delete(query)
        # Delete event from user owner
        await self.users.pull_array(
            {"email": email}, "myEvents", {"eventId": event_id})
        # Delete from organization
        await self.organizations.pull_array(
            {"organizationUrl": event["organizationUrl"]},
            "events", {"eventId": event_id})

        return self.check_deleted(deleted_count)

    async def collaborators(
            self, event_id: str, collaborator_email: str) -> dict:
        """
        Dellete a collaborator.

        Params:
        ------
        event_id: str - The uuid of the target event.
        collaborator_email: str - The email of the target collaborator.

        Return:
        ------
        {deleted: bool} - True if deleted, False if nothig happens.
        """

        query = _make_query(event_id)
        modified_count = await self.crud.pull_array(
            query=query,
            array_name="collaborators",
            condition={"email": collaborator_email})

        await self.users.pull_array(
            query={"email": collaborator_email},
            array_name="collaborations",
            condition={"eventId": event_id}
        )
        return self.check_deleted(modified_count)

    async def associates(self, event_id: str, associate_id: str) -> dict:
        """
        Dellete a associated.

        Params:
        ------
        event_id: str - The uuid of the target event.
        associate_id: str - The uuid of the target associated.

        Return:
        ------
        {deleted: bool} - True if deleted, False if nothig happens.
        """
        query = _make_query(event_id)
        modified_count = await self.crud.pull_array(
            query=query,
            array_name="associates",
            condition={"associatedId": associate_id})
        return self.check_deleted(modified_count)

    async def days(self, event_id, day_id) -> None:
        """
        Dellete a day.

        Params:
        ------
        event_id: str - The uuid of the target event.
        day_id: str - The uuid of the target day.

        Return:
        ------
        {deleted: bool} - True if deleted, False if nothig happens.
        """
        query = _make_query(event_id)
        modfied_count = await self.crud.pull_array(
            query=query,
            array_name="agenda",
            condition={"dayId": day_id})

        return self.check_deleted(modfied_count)

    async def conference(
            self, event_id: str, day_id: str,
            conference_id: str, speaker_id: str) -> None:
        """
        Delete a existing conference.
        """
        query = {
            "eventId": event_id,
            "agenda.dayId": day_id}
        array = "agenda.$.conferences"
        condition = {"conferenceId": conference_id}
        await self.crud.pull_array(query, array, condition)
        await self.speakers(event_id, speaker_id)

    async def speakers(self, event_id: str, speaker_id: str) -> dict:
        """
        Dellete a speaker.

        Params:
        ------
        event_id: str - The uuid of the target event.
        speaker_id: str - The uuid of the target speaker.
        """
        query = _make_query(event_id)
        condition = {"speakerId": speaker_id}
        await self.crud.pull_array(query, "speakers", condition)

    def check_deleted(self, count: int) -> dict:
        """
        Check if the count is grather than 0
        """
        if not count:
            return False
        return {"deleted": bool(count)}
