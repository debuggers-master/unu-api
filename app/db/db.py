"""
Db - Monglo Client instance and DB connection.
"""

import json
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import dumps
from bson import BSON

from config import settings  # pylint: disable-msg=E0611


###########################################
##             DB Connection             ##
###########################################

CLUSTER = settings.DB_CLUSTER
NAME = settings.DB_NAME
USER = settings.DB_USERNAME
PASSWORD = settings.DB_PASSWORD
CONFIG = "retryWrites=true&w=majority"

connection_str = f"mongodb+srv://{USER}:{PASSWORD}@{CLUSTER}/{NAME}?{CONFIG}"
client = AsyncIOMotorClient(connection_str)

# Get dabase
db = client[settings.DB_NAME]


###########################################
##         Collection Instance           ##
###########################################

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


###########################################
##             Parser Functions          ##
###########################################

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


###########################################
##         Injectable CRUD Class         ##
###########################################
class CRUD:
    """
    Crud operations.

    Params:
    ------
    collection: mongo_collection
        The mongo collection for CRUD
    """

    def __init__(self, collection):
        """
        Collection injection on initialzation.
        """
        self.coll = collection

    async def create(self, document_data: dict) -> str:
        """
        Create a new document in collection.
        """
        created = await self.coll.insert_one(document_data)
        return str(created.inserted_id)

    async def update(self, query: dict, document_data: dict) -> int:
        """
        Update an existing document.
        """
        updated = await self.coll.update_one(query, {"$set": document_data})
        return int(updated.modified_count)

    async def add_to_set(self, query: dict, array_name: str, data: any) -> int:
        """
        Add a new item to a list within a document.
        """
        operation = {"$addToSet": {f"{array_name}": data}}
        updated = await self.coll.update_one(query, operation)
        return int(updated.modified_count)

    async def push_nested(self, query: dict, path: str, data: any) -> int:
        """
        Insert a new document in nested element.
        """
        operation = {"$push":  {f"{path}": data}}
        updated = await self.coll.update_one(query, operation)
        return int(updated.modified_count)

    async def pull_array(
            self, query: dict, array_name: str, condition: dict) -> int:
        """
        Remove a item from a list that matches the condition.
        """
        operation = {"$pull": {f"{array_name}": condition}}
        updated = await self.coll.update_one(query, operation)
        return int(updated.modified_count)

    async def delete(self, query: dict) -> int:
        """
        Delete a existing document.
        """
        deleted = await self.coll.delete_one(query)
        return int(deleted.deleted_count)

    async def delete_many(self, query: dict) -> None:
        """
        Delete many documents.
        """
        await self.coll.delete_many(query)

    async def find(
            self, query: dict,
            only_one: bool = True,
            filters: List[str] = None,
            excludes: List[str] = None,
    ) -> dict:
        """
        Retrieve the data that matches with the query and the filters.
        """
        # Create the query filter
        query_filter = None
        if filters is not None:
            query_filter = self.generate_query_filter(filters)
        if excludes is not None:
            query_filter = self.generate_query_filter(excludes, excludes=True)

        # For find a single document
        if only_one:
            document = await self.coll.find_one(query, query_filter)
            return jsonify(document)

        # For find multiple documents
        cursor = self.coll.find(query, query_filter)
        items = []
        for document in await cursor.to_list(length=100):
            items.append(document)

        return items

    def generate_query_filter(
            self, filter_list: list = None, excludes: bool = False) -> dict:
        """
        Generate a dict with the correct mongo query filter
        """

        objet_filter = {}
        if filter_list is not None:
            for key in filter_list:
                if excludes:
                    objet_filter[key] = 0
                else:
                    objet_filter[key] = 1

        return objet_filter
