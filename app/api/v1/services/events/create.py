"""
Bussines Logic for create events elemets.
"""

from db.db import get_collection
from .utils import _uuid, _make_query, events_crud


# COLLECTIONS
PARTICIPANTS_COLLECTION_NAME = "participants"
participants_collection = get_collection(PARTICIPANTS_COLLECTION_NAME)


class CreateEvent:
    """
    Methos for create event elements.
    """

    def __init__(self):
        self.crud = events_crud

    async def create_event(self, event_data: dict) -> dict:
        """
        Creare a new event.

        Params:
        ------
        event_data: dict - The event info.

        Return:
        ------
        event_id: dict - The event uuid created.
        """
        event_id = _uuid()
        organization_name = event_data.get("organizationName")
        organization_url = organization_name.replace(" ", "-").lower()

        event_data.update({"eventId": event_id})
        event_data.update({"organizationUrl": organization_url})
        event_data.update({"organizationName": organization_name})
        event_data.update({"titleHeader": ""})
        event_data.update({"shortDescription": ""})
        event_data.update({"description": ""})
        event_data.update({"imageHeader": ""})
        event_data.update({"imageEvent": ""})
        event_data.update({"localTime": ""})
        event_data.update({"speakers": []})
        event_data.update({"collaborators": []})
        event_data.update({"associates": []})
        event_data.update({"publicationStatus": 0})
        event_data.update({"agenda": [{
            "dayID": _uuid(),
            "date": event_data.get("startDate"),
            "conferences": []
        }]})

        inserted_id = await self.crud.create(event_data)
        if not inserted_id:
            return False

        await participants_collection.insert_one(
            {"eventId": event_id, "emails": []})
        return {"eventId": event_id}

    async def add_collaborator(
            self, event_id: str, collaborator_data: dict) -> dict:
        """
        Add new collaborator to the event.

        Params:
        ------
        event_id: str - The event uuid.
        collaborator_data: str -  The principal collaborator data.

        Return:
        ------
        collaboratorId: The uuid of the created collaborator.
        """
        collaborator_id = _uuid()
        collaborator_data.update({"collaboratorId": collaborator_id})

        ##########################
        ##Logic for collaborator##
        #########################

        query = _make_query(event_id)
        modified_count = await self.crud.add_to_set(
            query, "collaborators", collaborator_data)
        if not modified_count:
            return False
        return {"collaboratorId": collaborator_id}

    async def add_speaker(self, event_id: str, speaker_data: dict) -> dict:
        """
        Add new speaker to the event.

        Params:
        ------
        event_id: str - The event uuid.

        Return:
        ------
        speaker_id: The uuid of the created speaker.
        """
        speaker_id = _uuid()
        speaker_data.update({"speakerId": speaker_id})
        query = _make_query(event_id)
        modified_count = await self.crud.add_to_set(
            query, "speakers", speaker_data)
        if not modified_count:
            return False
        return {"speakerId": speaker_id}

    #########################
    # Create agenda (Falta) #
    #########################

    async def add_associates(self, event_id: str, associate_data: dict) -> dict:
        """
        Add a new associated to event.

        Params:
        ------
        event_id: str - The event uuid.
        associate_data: dict - The new associated data.

        Return:
        ------
        associate_id: str - The uuid of the created associated.
        """
        associate_id = _uuid()
        associate_data.update({"associateId": associate_id})
        query = _make_query(event_id)
        modified_count = await self.crud.add_to_set(
            query, "associates", associate_data)
        if not modified_count:
            return False
        return {"associateId": associate_id}
