"""
Bussines Logic for update events elemets.
"""

from storage.service import upload_file
from .utils import _make_query, events_crud


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

    async def collaborators(
            self, event_id: str, collaborator_id: str, new_data: dict) -> dict:
        """
        Update one collaborator info.

        Params:
        ------
        event_id: str - The uuid of the target event.
        collaborator_email: str - The email of the target collaborator.
        new_data: dict - The new data for update.

        Return:
        ------
        {modified_count: n} - The number (n) of modified items.
        """
        for key, value in list(new_data.items()):
            if value is None:
                del new_data[key]

        # Update in the collection
        query = {"eventId": event_id,
                 "collaborators.collaboratorId": collaborator_id}
        data = {"collaborators.$": new_data}
        modified_count = await self.crud.update(query, data)
        return self.check_modified(modified_count)

    async def speakers(
            self, event_id: str, speaker_id: str, new_data: dict) -> dict:
        """
        Update the speakers data.

        Params:
        ------
        event_id: str - The uuid of the target event.
        speaker_id: str - The uuid of the target speaker.
        new_data: dict - The new data for update.

        Return:
        ------
        {modified_count: n} - The number (n) of modified items.
        """
        query = {"event_id": event_id, "speakers.speakerId": speaker_id}
        data = {"speakers.$": new_data}
        modified_count = await self.crud.update(query, data)
        return self.check_modified(modified_count)

    async def associates(
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
        query = {"event_id": event_id,
                 "associates.associatedId": associated_id}
        data = {"associates.$": new_data}
        modified_count = await self.crud.update(query, data)
        return self.check_modified(modified_count)

    ###################
    ## Agenda (Falta)##
    ###################

    async def chnage_status(
            self, event_id: str, actual_status: bool) -> dict:
        """
        Change the actual a publication status.

        Params:
        ------
        event_id: str - The event uuid.
        actual_status: bool - The actual publication status.

        Return: True
        """
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
