"""
DB participants - Db functions about participants
"""

from bson.json_util import ObjectId
from .db import get_collection, jsonify

# Users collection
db = get_collection('participants')


# -------------------- Participants methods -------------------- #

async def create_new_participants_document(event_id: str) -> str:
    """
    Create a new document that store a particpats of and event

    Params:
    ------
    event_id: str
        The event id in wich the participants are stored.

    Return:
      inserted_id: str
          The new document id.
    """

    document = {"event_id": event_id, "participants": []}
    created = await db.insert_one(document)
    return str(created.inserted_id)


async def add_participant(event_id: str, participant_data: dict) -> str:
    """
    Add a new participant to the event participants list.

    Params:
    ------
    event_id: str
        The event id in wich the participants are stored.
    participant_data: dict
        The participant data

    Return:
    ------
    modified_count: str
        The modified documents count (always str(1))
    """

    query = {"event_id": ObjectId(event_id)}
    operation = {"$addToSet": {"participants": participant_data}}
    updated = db.update_one(query, operation)
    return str(updated.modified_count)


async def get_participants(event_id: str) -> list:
    """
    Get all participants of an event.

    Params:
    ------
    event_id: str
        The event id.

    Return:
    ------
    participants_list: list
        The participants list
    """

    query = {"event_id": ObjectId(event_id)}
    participants = db.find(query, {"participants": 1})
    return participants
