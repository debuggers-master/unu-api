"""
Db - Monglo Client instance and DB connection.
"""

import json
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from bson.json_util import dumps
from bson import BSON

from error_logger.main import error_logger
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

try:
    client = AsyncIOMotorClient(connection_str)
except Exception as ex:  # pylint: disable-msg=W0703
    error_logger.register(ex)

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
        try:
            created = await self.coll.insert_one(document_data)
        except Exception as ex:  # pylint: disable-msg=W0703
            await error_logger.register(ex)
        return str(created.inserted_id)

    async def update(
            self, query: dict, document_data: dict, many: bool = False) -> int:
        """
        Update an existing document.
        """
        if many:
            try:
                updated = await self.coll.update_many(
                    query, {"$set": document_data})
            except Exception as ex:  # pylint: disable-msg=W0703
                await error_logger.register(ex)
        else:
            try:
                updated = await self.coll.update_one(
                    query, {"$set": document_data})
            except Exception as ex:  # pylint: disable-msg=W0703
                await error_logger.register(ex)
        return int(updated.modified_count)

    async def add_to_set(self, query: dict, array_name: str, data: any) -> int:
        """
        Add a new item to a list within a document.
        """
        operation = {"$addToSet": {f"{array_name}": data}}
        try:
            updated = await self.coll.update_one(query, operation)
        except Exception as ex:  # pylint: disable-msg=W0703
            await error_logger.register(ex)
        return int(updated.modified_count)

    async def push_nested(self, query: dict, path: str, data: any) -> int:
        """
        Insert a new document in nested element.
        """
        operation = {"$push":  {f"{path}": data}}
        try:
            updated = await self.coll.update_one(query, operation)
        except Exception as ex:  # pylint: disable-msg=W0703
            await error_logger.register(ex)
        return int(updated.modified_count)

    async def pull_array(
            self, query: dict, array_name: str,
            condition: dict, many: bool = False) -> int:
        """
        Remove a item from a list that matches the condition.
        """
        operation = {"$pull": {f"{array_name}": condition}}
        if many:
            try:
                updated = await self.coll.update_many(query, operation)
            except Exception as ex:  # pylint: disable-msg=W0703
                await error_logger.register(ex)
        else:
            try:
                updated = await self.coll.update_one(query, operation)
            except Exception as ex:  # pylint: disable-msg=W0703
                await error_logger.register(ex)
        return int(updated.modified_count)

    async def delete(self, query: dict) -> int:
        """
        Delete a existing document.
        """
        try:
            deleted = await self.coll.delete_one(query)
        except Exception as ex:  # pylint: disable-msg=W0703
            await error_logger.register(ex)
        return int(deleted.deleted_count)

    async def delete_many(self, query: dict) -> None:
        """
        Delete many documents.
        """
        try:
            await self.coll.delete_many(query)
        except Exception as ex:  # pylint: disable-msg=W0703
            await error_logger.register(ex)

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
            try:
                document = await self.coll.find_one(query, query_filter)
            except Exception as ex:  # pylint: disable-msg=W0703
                await error_logger.register(ex)
            return jsonify(document)

        # For find multiple documents
        try:
            cursor = self.coll.find(query, query_filter)
            items = []
            for document in await cursor.to_list(length=100):
                items.append(document)
        except Exception as ex:  # pylint: disable-msg=W0703
            await error_logger.register(ex)

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
