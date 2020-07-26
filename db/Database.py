import pymongo
from bson.objectid import ObjectId
import logging
from typing import Union


class Database(object):
    """
        Class to operate CRUD with mongodb
    """

    def __init__(self, mongo_uri, db_name):
        """
            Constructor for class
            default to localhost with port 27017
            default to database name of gluster
        """
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = None
    
    def __del__(self):
        try:
            self.client.close()
        except Exception:
            pass

    def set_collection(self, collection: str):
        """
            set the collection to operate

            ARGS:
                collection: str -> name of the collection

            RETURNS:
        """
        if not isinstance(collection, str):
            raise TypeError("Collection need to be string type")
        self.collection = self.db[collection]

    def insert(self, payload: dict):
        """
            operate insert to mongodb

            ARGS:
                payload: dict -> data to be inserted to the db

            RETURNS:

        """
        if not isinstance(payload, dict):
            raise TypeError("payload need to be dict type, get type {}".format(type(payload)))

        try:
            self.collection.insert_one(payload)
        except Exception as err:
            logging.exception(
                "Not able to insert data : {payload} to collection : {collection} with {msg}".format(payload=payload, collection=self.collection, msg=err.__str__()))
            raise

    def find_by_id(self, id: Union[str, ObjectId]) -> dict:
        """
            find one document using id

            ARGS:
                id: str, ObjectId -> id to look up

            RETURNS:
                bool
        """
        if not isinstance(id, (str, ObjectId)):
            raise TypeError("id need to be str or ObjectId type")

        if isinstance(id, str):
            id = ObjectId(id)

        try:
            result = self.collection.find_one({"_id": id})
            return result
        except Exception as err:
            logging.exception(
                "Not able to find using id : {id} from collection : {collection} with {msg}".format(id=id.toString(), collection=self.collection, msg=err.__str__()))
            raise

    def find_all(self, filter: dict=None) -> list:
        """
            find all document from collection

            ARGS:
                NONE

            RETURNS:
                list -> list of documents
        """
        try:
            if filter is None:
                return list(self.collection.find())
            else:
                if not isinstance(filter, dict):
                    raise TypeError("filter need to be dict type, received type of : {}".format(type(dict)))
                return list(self.collection.find({}, filter))
        except Exception as err:
            logging.exception(
                "Not able to find_all from collection : {collection} with {msg}".format(collection=self.collection, msg=err.__str__()))
            raise

    def find(self, query: dict) -> dict:
        """
            find using query

            ARGS:
                query: dict -> query string

            RETURNS:
                list -> list of document
        """
        if not isinstance(query, dict):
            raise TypeError("query need to be dict type")

        try:
            result = list(self.collection.find(query))
            return result
        except Exception as err:
            logging.exception(
                "Not able to find by query : {query} from collection : {collection} with {msg}".format(query=query, collection=self.collection, msg=err.__str__()))
            raise

    def update(self, id: Union[str, ObjectId], payload: dict) -> bool:
        if not isinstance(id, (str, ObjectId)):
            raise TypeError("id need to be str or ObjectId type")

        if isinstance(id, str):
            id = ObjectId(id)

        if not isinstance(payload, dict):
            raise TypeError("payload need to be dict type, get type {}".format(type(payload)))
        
        try:
            self.collection.update_one({"_id": id}, {"$set": payload})
        except Exception as err:
            logging.exception("Not able to update _id : {id}, in collection : {collection} with {msg}".format(id=id, collection=self.collection, msg=err.__str__()))
            raise
