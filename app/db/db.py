"""
Db - Monglo Client instance and DB connection.
"""

import json
from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import dumps
from bson import BSON

from config import settings

# Instance the motor-mongo client
CLUSTER = settings.DB_CLUSTER
NAME = settings.DB_NAME
USER = settings.DB_USERNAME
PASSWORD = settings.DB_PASSWORD
CONFIG = "retryWrites=true&w=majority"

connection_str = f"mongodb+srv://{USER}:{PASSWORD}@{CLUSTER}/{NAME}?{CONFIG}"
client = AsyncIOMotorClient(connection_str)

# Get dabase
db = client[settings.DB_NAME]


# ------------------- DB Collection and Parcer bson ------------------- #

def get_collection(collection_name: str):
    """
    Return a mongo db collection instance.

    Params
    ------
    collection_name: str
        The mongo db collection name.

    Returns
    -------
    collection: Class
        The mongo db collection instance
    """

    collection = db[collection_name]
    return collection


def jsonify(data: BSON) -> dict:
    """
    Dumps a bson to json object.

    Params
    ------
    data: bson
        The mongo db bson data.

    Returns
    -------
    json_object: json
        The mongo data dumped to a json object
    """

    return json.loads(dumps(data))


# ------------------------ CRUD class ------------------------ #
class CRUD:
    """
    Crud operations.

    Params:
    ------
    collection: mongo_collection
        The mongo collection for CRUD
    """

    def __init__(self, collection):
        self.coll = collection

    async def create(self, document_data: dict) -> str:
        """
        Create a new document in collection.
        """
        created = self.coll.insert_one(document_data)
        return str(created.inserted_id)

    async def update(self, query: dict, document_data: dict) -> str:
        """
        Update an existing document.
        """
        updated = self.coll.update_one(query, {"$set": document_data})
        return str(updated.modified_count)

    async def add_to_set(self, query: dict, array_name: str, data: any) -> str:
        """
        Add a new item to a list within a document.
        """
        operation = {"$addToSet": {f"{array_name}": data}}
        updated = self.coll.update_one(query, operation)
        return str(updated.modified_count)

    async def delete(self, query: dict) -> None:
        """
        Delete a existing document
        """

        await self.coll.delete_one(query)
