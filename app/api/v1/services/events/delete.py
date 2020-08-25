"""
Bussines Logic for update events elemets.
"""

from .utils import _make_query, events_crud


class DeleteEvent:
    """
    Methods for delete event elemnts.
    """

    def __init__(self):
        self.crud = events_crud

    async def all(self, event_id: str) -> dict:
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

    async def collaborators(self, event_id: str, collaborator_id: str) -> dict:
        """
        Dellete a collaborator.

        Params:
        ------
        event_id: str - The uuid of the target event.
        collaborator_id: str - The uuid of the target collaborator.

        Return:
        ------
        {deleted: bool} - True if deleted, False if nothig happens.
        """

        query = _make_query(event_id)
        modified_count = await  self.crud.pull_array(
            query= query,
            array_name="collaborators",
            condition={"collaboratorId": collaborator_id})
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
        modified_count =  await self.crud.pull_array(
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
