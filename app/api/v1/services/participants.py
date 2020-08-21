"""
Bussiness login about user particpants.
"""

from uuid import uuid4
from db.db import get_collection, CRUD

# COLLECTIONS
PARTICIPANTS_COLLECTION_NAME = "participants"

# DB collection instances
participants_collection = get_collection(PARTICIPANTS_COLLECTION_NAME)


# ------------------ User controller operations ----------------- #
class ParticipantsServices:
    """
    Opeartions about participants
    """

    def __init__(self):
        self.crud = CRUD(participants_collection)

    async def register(self, event_id: str, particpant_email: str, participant_name: str) -> dict:
        """
        Register a participant to a specific event.

        Params:
        ------
        event_id: str - The specific event uuid
        particpant_email: str - The email of the particpant
        participant_name: str - The participant name

        Return:
        {registered: True}
        """
        query = {"eventId": event_id}
        data = {"name": participant_name, "email": particpant_email}
        modified_count = await self.crud.add_to_set(query, "emails", data)
        return {"registered": bool(modified_count)}
