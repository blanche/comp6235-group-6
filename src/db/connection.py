from pymongo import MongoClient


class DbConnection:
    host = "localhost"
    port = 27017
    db = "restaurant_data"
    client = None

    def __init__(self):
        self.get_connection_to_db()

    @classmethod
    def get_connection_to_db(cls):
        if cls.client is None:
            cls.client = MongoClient(cls.host, cls.port)
        return cls.client

    def get_restaurant_db(self):
        return self.client.restaurant_data

    def __del__(self):
        self.client.close()
