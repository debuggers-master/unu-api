"""
Commun utils to manage events.
"""

from uuid import uuid4

from db.db import get_collection, CRUD


# COLLECTIONS
EVENTS_COLLECTION_NAME = "events"
PARTICIPANTS_COLLECTION_NAME = "participants"


# DB collection instances
events_collection = get_collection(EVENTS_COLLECTION_NAME)
events_crud = CRUD(events_collection)

participants_collection = get_collection(PARTICIPANTS_COLLECTION_NAME)


# --------------- Functions -------------------- #

def _make_query(event_id: str) -> dict:
    """
    Return the event query: {"eventId": event_id}
    """
    return {"eventId": event_id}


def _uuid() -> str:
    """
    Return a unique uuid
    """
    return str(uuid4())
