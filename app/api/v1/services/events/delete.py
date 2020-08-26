"""
Bussines Logic for update events elemets.
"""

from db.db import get_collection, CRUD
from .utils import _make_query, events_crud


# COLLECTIONS
PARTICIPANTS_COLLECTION_NAME = "participants"
participants_collection = get_collection(PARTICIPANTS_COLLECTION_NAME)
PARTICIPANTS_COLLECTION_NAME = "users"
users_collection = get_collection(PARTICIPANTS_COLLECTION_NAME)


class DeleteEvent:
    """
    Methods for delete event elemnts.
    """

    def __init__(self):
        self.crud = events_crud
        self.users = CRUD(users_collection)
        self.participants = CRUD(participants_collection)

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
        deleted_count = await self.crud.delete(query)
        await self.participants.delete(query)
        await self.users.pull_array(
            {"email": email}, "myEvents", {"eventId": event_id})
        return self.check_deleted(deleted_count)

    async def speakers(self, event_id: str, speaker_id: str) -> dict:
        """
        Dellete a speaker.

        Params:
        ------
        event_id: str - The uuid of the target event.
        speaker_id: str - The uuid of the target speaker.

        Return:
        ------
        {deleted: bool} - True if deleted, False if nothig happens.
        """
        query = _make_query(event_id)
        condition = {"speakerId": speaker_id}
        modified_count = self.crud.pull_array(query, "speakers", condition)
        return self.check_deleted(modified_count)

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
            condition={"associateId": associate_id})
        return self.check_deleted(modified_count)

    def check_deleted(self, count: int) -> dict:
        """
        Check if the count is grather than 0
        """
        if not count:
            return False
        return {"deleted": bool(count)}
