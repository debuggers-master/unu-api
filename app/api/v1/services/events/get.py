"""
Bussines Logic for find and retrieve events.
"""

from typing import List
from datetime import date, datetime

from db.db import get_collection, CRUD
from .utils import _make_query

# COLLECTIONS
EVENTS_COLLECTION_NAME = "events"
PARTICIPANTS_COLLECTION_NAME = "participants"


# DB collection instances
events_collection = get_collection(EVENTS_COLLECTION_NAME)
events_crud = CRUD(events_collection)

participants_collection = get_collection(PARTICIPANTS_COLLECTION_NAME)


class GetEvent:
    """
    Methos for retrieve events information.
    """

    def __init__(self):
        self.crud = events_crud
        self.participants = participants_collection

    async def get_event(
            self,
            event_id: str,
            filters: List[str] = None,
            excludes: List[str] = None) -> dict:
        """
        Return the event that matches with the querys.

        Params:
        ------
        event_id: str - The event id
        filters: List[str] - The fields that you want to retrieve.
        exclide: List[str] - The fields that you want to exclude

        Return:
        ------
        event: list - The event data
        """
        query = _make_query(event_id)
        event = await self.crud.find(query, filters=filters, excludes=excludes)
        return event

    async def get_event_from_url(
            self,
            organization_name: str,
            event_url: str,
            filters: List[str] = None,
            excludes: List[str] = None) -> dict:
        """
        Return the event that matches with the query.

        Params:
        ------
        event_id: str - The event id
        filters: List[str] - The fields that you want to retrieve.
        exclude: List[str] - The fields that you want to exclude

        Return:
        ------
        event_list: list- A list with all events finded.
        """

        query = {"organizationUrl": organization_name, "url": event_url}
        event = await self.crud.find(
            query, filters=filters, excludes=excludes)

        if event:
            if not event.get("publucationStatus"):
                return False
            return event
        return False

    async def get_published_events(self) -> list:
        """
        Return all published events with a date major than today.

        Return:
        ------
        events: - List[EventOut] - a list of events.
        """
        # now = datetime.now()
        # today = date(now.year, now.month, now.day)
        query = {"publicationStatus": 1}
        filters = ["eventId", "name", "startDate", "organizationName"]
        events = await self.crud.find(query, only_one=False, filters=filters)
        return events

    async def get_count_particpants(self, event_id: str) -> int:
        """
        Return the number of inscribed participants.

        Params:
        ------
        event_id: str - The unique event uuid

        Return:
        ------
        count: int - The number of particpants
        """
        count = await self.participants.find_one({"eventId": event_id})
        return {"participants": len(count.get("emails"))}

    async def get_particpants(self, event_id: str) -> int:
        """
        Return the list of inscribed participants.

        Params:
        ------
        event_id: str - The unique event uuid

        Return:
        ------
        participants: int - The list of particpants
        """
        participnats = await participants_collection.find_one({"eventId": event_id})
        return participnats.get("emails")
