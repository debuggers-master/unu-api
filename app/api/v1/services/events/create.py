"""
Bussines Logic for create events elemets.
"""

from db.db import get_collection, CRUD
from storage.service import upload_file
from schemas.users import EventUserBaseDB
from schemas.events.event import EventInUser
from schemas.events.collaborators import CollaboratorInfo
from schemas.events.speakers import SpeakerInfo
from auth.services import register_user

from .utils import _uuid, _make_query, events_crud


###########################################
##          Collection Instances         ##
###########################################

participants_collection = get_collection("participants")
users_collection = get_collection("users")
organizations_collection = get_collection("organizations")


###########################################
##        Events - Create Service        ##
###########################################
class CreateEvent:
    """
    Methods for create event elements.
    """

    def __init__(self):
        self.crud = events_crud
        self.users = CRUD(users_collection)
        self.participants = CRUD(participants_collection)
        self.organizations = CRUD(organizations_collection)

    async def create_event(self, event_data: dict, user_email: str) -> dict:
        """
        Creare a new event.

        Params:
        ------
        event_data: dict - The event info.

        Return:
        ------
        event_id: dict - The event uuid created.
        """
        
        #Check url exits
        query_url = {"organizationName": event_data.get("organizationName"),
                 "url":event_data.get("url")}
        same_url_in_org = await self.crud.find(query_url)

        if same_url_in_org:
            return 409

        event_id = _uuid()

        # Create the correct organization url
        organization_name = event_data.get("organizationName")
        organization_url = organization_name.replace(" ", "-").lower()

        # Add all void structure
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
        event_data.update({"publicationStatus": False})
        event_data.update({"agenda": [{
            "dayId": _uuid(),
            "date": event_data.get("startDate"),
            "conferences": []
        }]})

        # Create the event
        inserted_id = await self.crud.create(event_data)
        if not inserted_id:
            return False

        # Add participants collections
        await self.participants.create({
            "eventId": event_id, "emails": []})

        # Update myEvents in User collection
        event_in_user = EventUserBaseDB(**event_data)
        await self.users.add_to_set(
            {"email": user_email}, "myEvents", event_in_user.dict())

        # Update in the organization
        data = {"eventId": event_id, "name": event_data["name"]}
        await self.organizations.add_to_set(
            {"organizationName": organization_name}, "events", data)

        return {"eventId": event_id}

    async def add_collaborator(
            self, event_id: str, collaborator_data) -> dict:
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
        # Make sure the user is new
        user = await self.users.find({"email": collaborator_data.email})
        if user:
            return 409

        # Add the user as collaborator to an existing event
        collaborator_to_event = CollaboratorInfo(**collaborator_data.dict())
        query = _make_query(event_id)
        modified_count = await self.crud.add_to_set(
            query, "collaborators", collaborator_to_event.dict())

        if not modified_count:
            # The event doesn't exist
            return 404

        # Only regitered if the event is valid
        collaborator = await register_user(collaborator_data)

        # Add the event to user collaborations
        event = await self.crud.find(query)
        collaboration_in_user = EventInUser(**event)
        await self.users.add_to_set(
            {"email": collaborator_data.email},
            "collaborations",
            collaboration_in_user.dict())

        return {"collaboratorId": collaborator.userId}

    async def add_existing_collaborator(
            self, event_id: str, email: str) -> dict:
        """
        Add existing collaborator to the event.

        Params:
        ------
        event_id: str - The event uuid.
        email: str -  The user email.

        Return:
        ------
        collaboratorId: The uuid of the created collaborator.
        """
        # Find user and carry on only if the user exists
        user = await self.users.find({"email": email})
        if not user:
            return 412

        # Add the user to event collaborator
        collaborator_to_event = CollaboratorInfo(**user)
        query = _make_query(event_id)
        await self.crud.add_to_set(
            query, "collaborators", collaborator_to_event.dict())

        # Add the event to user collaborations
        event = await self.crud.find(query)
        collaboration_in_user = EventInUser(**event)
        await self.users.add_to_set(
            {"email": email}, "collaborations", collaboration_in_user.dict())

        return {"collaboratorId": user["userId"]}

    async def add_conference(
            self, event_id: str, day_id: str, conference_data: dict) -> dict:
        """
        Add a new conference to some specific day

        Params:
        ------
        event_id: str - The event uuid
        day_id: str -  The day id
        confernce_data: dict - The conference data

        Return:
        ------
        conferenceId: str - The new conference id
        speakerId: str -  The new speaker id
        """
        conference_id = _uuid()
        speaker_id = _uuid()
        conference_data.update({"conferenceId": conference_id})
        conference_data.update({"speakerId": speaker_id})

        # Image proccessing
        image_url = await self.upsert_image(conference_data["speakerPhoto"])
        conference_data.update({"speakerPhoto": image_url})

        # Add conference
        query = {"eventId": event_id, "agenda.dayId": day_id}
        path = "agenda.$.conferences"
        pushed = await self.crud.push_nested(query, path, conference_data)
        if not pushed:
            return False

        # Add speaker separatly
        speaker_data = SpeakerInfo(**conference_data).dict()
        await self.add_speaker(event_id, speaker_data, speaker_id)

        return {"conferenceId": conference_id, "speakerId": speaker_id}

    async def add_speaker(
            self, event_id: str, speaker_data: dict, speaker_id: str) -> dict:
        """
        Add new speaker to the event.

        Params:
        ------
        event_id: str - The event uuid.

        Return:
        ------
        speaker_id: The uuid of the created speaker.
        """
        existing_speaker = await self.crud.find(
            {"eventId": event_id, "speakers.twitter": speaker_data["twitter"]})
        if existing_speaker:
            return None
        # Only add if the speaker is new
        speaker_data.update({"speakerId": speaker_id})
        query = _make_query(event_id)
        await self.crud.add_to_set(query, "speakers", speaker_data)

    async def add_day(self, event_id: str, day_data: dict) -> dict:
        """
        Add a new day to agenda.

        Params:
        ------
        event_id: str - The event uuid.
        day_data: dict - The day data

        Return:
        ------
        dayId: The uuid of the day
        """
        day_id = _uuid()
        day_data.update({"dayId": day_id})
        day_data.update({"conferences": []})

        # Verify the date is not the same
        day = await self.crud.find(
            {"eventId": event_id, "agenda.date": day_data["date"]})
        if day:
            return False

        # Add the new day
        query = _make_query(event_id)
        modified_count = await self.crud.add_to_set(query, "agenda", day_data)
        if not modified_count:
            return False
        return {"dayId": day_id}

    async def add_associates(self, event_id: str, associated_data) -> dict:
        """
        Add a new associated to event.

        Params:
        ------
        event_id: str - The event uuid.
        associated_data: dict - The new associated data.

        Return:
        ------
        associate_id: str - The uuid of the created associated.
        """
        associated_id = _uuid()
        associated_data.update({"associatedId": associated_id})

        # Image processing
        logo_url = await self.upsert_image(associated_data.get("logo"))
        associated_data.update({"logo": logo_url})

        query = _make_query(event_id)
        modified_count = await self.crud.add_to_set(
            query, "associates", associated_data)

        if not modified_count:
            return False
        return {"associatedId": associated_id}

    async def upsert_image(self, image: str) -> str:
        """
        Update the url for image if it is new.
        """
        prefix = image.split(":")[0]
        if prefix == "data":
            new_image_url = await upload_file(file_base64=image)
            return new_image_url
        if prefix in ("http", ""):
            return image
        return image
