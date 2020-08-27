"""
Bussiness login about user particpants.
"""

from db.db import get_collection, CRUD

###########################################
##       Users Collection Instance       ##
###########################################

PARTICIPANTS_COLLECTION_NAME = "participants"
participants_collection = get_collection(PARTICIPANTS_COLLECTION_NAME)


###########################################
##      Participants Service Class       ##
###########################################

class ParticipantsServices:
    """
    Opeartions about participants
    """

    def __init__(self):
        """
        Crud instance of the participants collection.
        """
        self.crud = CRUD(participants_collection)

    async def register(self, event_id: str, particpant_email: str) -> dict:
        """
        Register a participant to a specific event.

        Params:
        ------
        event_id: str - The specific event uuid
        particpant_email: str - The email of the particpant

        Return:
        {registered: True}
        """
        query = {"eventId": event_id}
        data = particpant_email
        modified_count = await self.crud.add_to_set(query, "emails", data)
        return {"registered": bool(modified_count)}
