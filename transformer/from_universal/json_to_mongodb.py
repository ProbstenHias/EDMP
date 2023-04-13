from json_to_data import JsonToData
from pymongo import MongoClient


class JsonToMongoDB(JsonToData):
    def __init__(self) -> None:
        self.client = None
        self.database = None
        self.collection = None

    def connect(self, dbname, user, password, host, port):
        connection_string = f"mongodb://{user}:{password}@{host}:{port}/{dbname}"
        self.client = MongoClient(connection_string)
        self.database = self.client[dbname]

    def disconnect(self):
        self.client.close()

    def prepare_data(self, json_data):
        return json_data

    def insert_data(self, data):
        self.collection.insert_many(data)

    def create_table(self, json_data, table_name):
        self.collection = table_name
