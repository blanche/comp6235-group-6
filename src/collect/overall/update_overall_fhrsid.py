
from db.connection import DbConnection
import bson

def create_comments():
    """
    update overall collection with missing FHSID from hygine data
    """

    db = DbConnection().get_resturant_db()

    for doc in db.hygine_data.find({}):
        key = bson.son.SON({"FHRSID" : doc["FHRSID"]})
        data = bson.son.SON({"FHRSID" : doc["FHRSID"]})
        db.overall.update(key, data, upsert=True)


if __name__ == "__main__":
    create_comments()