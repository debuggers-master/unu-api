"""
Bussines Logic for update events elemets.
"""

from storage.service import upload_file
from schemas.events.speakers import SpeakerInfo
from .utils import _make_query, events_crud, get_collection


class UpdateEvent:
    """
    Methods for update event elemnts.
    """

    def __init__(self):
        self.crud = events_crud

    async def principal_info(self, event_id: str, new_data: dict) -> dict:
        """
        Update the principal event info.

        Params:
        ------
        event_id: str - The uuid of the target event.
        new_data: dict - The new data for update.

        Return:
        ------
        {modified_count: n} - The number (n) of modified items.
        """
        # Update image only if are new files
        image_header = await self.update_image(new_data["imageHeader"])
        image_event = await self.update_image(new_data["imageEvent"])
        new_data.update({"imageHeader": image_header})
        new_data.update({"imageEvent": image_event})

        query = _make_query(event_id)
        modified_count = await self.crud.update(query, new_data)
        return self.check_modified(modified_count)

    async def associateds(
            self, event_id: str, associated_id: str, new_data: dict) -> dict:
        """
        Update one associated info.

        Params:
        ------
        event_id: str - The uuid of the target event.
        associated_id: str - The uuid of the target associated.
        new_data: dict - The new data for update.

        Return:
        ------
        {modified_count: n} - The number (n) of modified items.
        """
        # Image processing
        associated_logo = await self.update_image(new_data.get("logo"))
        new_data.update({"logo": associated_logo})

        query = {"eventId": event_id,
                 "associates.associatedId": associated_id}
        data = {"associates.$": new_data}

        modified_count = await self.crud.update(query, data)
        return self.check_modified(modified_count)

    async def days(self, event_id: str, day_data: dict):
        """
        Update a existing day
        event_id: str - The event uuid.
        day_data: bool - The day date to update.

        Return:
        ------
        {modified_count: n} - The number (n) of modified items.
        """
        # Verify the date is not the same
        day = await self.crud.find({
            "eventId": event_id,
            "agenda.dayId": day_data["dayId"],
            "agenda.date": day_data["date"],
        })
        if day:
            # The date doesn't have changes
            return self.check_modified(False)

        day_couped = await self.crud.find({
            "eventId": event_id,
            "agenda.date": day_data["date"],
        })
        if day_couped:
            return False

        query = {"eventId": event_id, "agenda.dayId": day_data["dayId"]}
        data = {"agenda.$.date": day_data["date"]}
        modified_count = await self.crud.update(query, data)
        return self.check_modified(modified_count)

    async def conference(
            self, event_id: str, day_id: str, conference_data: dict) -> dict:
        """
        Update a  conference in some specific day

        Params:
        ------
        event_id: str - The event uuid
        day_id: str -  The day id
        confernce_data: dict - The conference data

        Return:
        ------
        {modified_count: n} - The number (n) of modified items.
        """
        # Image proccessing
        url_image = await self.update_image(conference_data["speakerPhoto"])
        conference_data.update({"speakerPhoto": url_image})

        conference_id = conference_data["conferenceId"]
        query = {
            "eventId": event_id,
            "agenda.dayId": day_id,
            "agenda.conferences.conferenceId": conference_id}

        data = {"agenda.$[].conferences.$": conference_data}
        conf_count = await self.crud.update(query, data)

        speaker_data = SpeakerInfo(**conference_data).dict()
        speaker_data.update({"speakerId": conference_data["speakerId"]})
        speaker_count = await self.speakers(event_id, speaker_data)

        return {"modifiedCount": conf_count + speaker_count}

    async def speakers(
            self, event_id: str, speaker_data: dict) -> dict:
        """
        Update the speakers data.

        Params:
        ------
        event_id: str - The uuid of the target event.
        speaker_data: dict - The new data for update.

        Return:
        ------
        {modified_count: n} - The number (n) of modified items.
        """
        query = {"eventId": event_id,
                 "speakers.speakerId": speaker_data["speakerId"]}
        data = {"speakers.$": speaker_data}
        modified_count = await self.crud.update(query, data)
        return modified_count

    async def change_status(
            self, event_id: str, actual_status: bool, email: str) -> dict:
        """
        Change the actual a publication status.

        Params:
        ------
        event_id: str - The event uuid.
        actual_status: bool - The actual publication status.
        email: str - The email of the current user

        Return: bool
        """
        __users = get_collection("users")
        user = __users.find({"email": email})
        user_events = user["myEvents"]
        is_user_admin = list(
            filter(lambda ev: ev.get("eventId") == event_id, user_events))
        is_user_admin = bool(is_user_admin[0])
        if not is_user_admin:
            return 403

        query = _make_query(event_id)
        status = not actual_status
        await self.crud.update(query, {"publicationStatus": status})
        return {"actualStatus": status}

    def check_modified(self, modified_count: int) -> dict:
        """
        Check if the modified_count is grather than 0
        """
        if not modified_count:
            return {"modifiedCount": 0}
        return {"modifiedCount": modified_count}

    async def update_image(self, image: str) -> str:
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
