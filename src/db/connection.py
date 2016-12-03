from pymongo import MongoClient


class DbConnection:
    # host = "localhost"
    # port = 27017
    # auth = False
    # db="resturant_data"
    host = "svm-lw4u16-comp6235-group-6.ecs.soton.ac.uk"
    port = 27018
    auth = True
    db = "restaurants"
    client = None

    def __init__(self):
        self.get_connection_to_db()

    @classmethod
    def get_connection_to_db(cls):
        if cls.client is None:
            cls.client = MongoClient(cls.host, cls.port)
        return cls.client

    def get_restaurant_db(self):
        db = self.client[self.db]
        if self.auth:
            db.authenticate('user', 'banana4')
        return db

    def get_yelp_collection(self, db=None):
        if db is None:
            db = self.get_restaurant_db()
        return db.yelp_data

    def get_hygiene_collection(self, db=None):
        if db is None:
            db = self.get_restaurant_db()
        return db.hygiene_data

    def get_overall_collection(self, db=None):
        if db is None:
            db = self.get_restaurant_db()
        return db.overall

    def __del__(self):
        self.client.close()
