"""
DB events - Db functions about events
"""

from bson.json_util import ObjectId
from .db import get_collection, CRUD

# Users collection
db = get_collection('events')
crud = CRUD(db)


# -------------------- Events methods -------------------- #

async def get_event(
        event_id: str, filters: list = None, excludes: list = None) -> dict:
    """
    Retrieve the complete information about one event.

    Params:
    ------
    event_id: str
        The event id.
    filters: list
        An array with the keys that you want to find.
        Only return the keys you passed.
    excludes: list
        An array with the keys you want to exclude from the result.
        Return all keys, except that passed in the excludes list.

    Return:
    ------
    event_data: dict
        The event data.
    """

    query = {"_id": ObjectId(event_id)}
    event_data = await crud.find(query, filters=filters, excludes=excludes)
    return event_data


async def create_event(event_data: dict) -> str:
    """
    Create a new event.

    Paramas:
    -------
    event_data: dict
        The event data for created.

    Return:
    ------
    inserted_id: str
        The inserted id of the created event
    """

    inserted_id = await crud.create(event_data)
    return inserted_id


async def update_event(event_id: str, event_data: dict) -> str:
    """
    Update a existing event.

    Paramas:
    -------
    event_data: dict
        The complete event data.

    Return:
    ------
    modified_counr: str
        The number of modified documents.
        (1 if updated, 0 if nothing happen)
    """
    #"¿Modificar para que se borre con event_ID ?"
    query = {"_id": ObjectId(event_id)}
    modified_count = await crud.update(query, event_data)
    return modified_count


async def delete_event(event_id: str) -> bool:
    """
    Delete a existing event.

    Paramas:
    -------
    event_data: dict
        The complete event data.

    Return:
    ------
    True
    """

    query = {"_id": ObjectId(event_id)}
    await crud.delete(query)
    return True
