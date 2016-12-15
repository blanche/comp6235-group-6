import bson

from src.db.connection import DbConnection
from util import setup_logger


def combine_yelp_to_overall():
    db = DbConnection().get_restaurant_db()
    yelp_data = DbConnection().get_yelp_collection(db)
    overall = DbConnection().get_overall_collection(db)

    yelp_logger = setup_logger("yelp")

    total = DbConnection().get_yelp_collection().count({"FHRSID": {"$exists": True}})
    bulk_op = overall.initialize_unordered_bulk_op()
    i = 0
    for yelp_entry in yelp_data.find({"FHRSID": {"$exists": True}}):
        add_to_overall = {
            "id": yelp_entry["id"],
            "price": yelp_entry["price"],
            "rating": yelp_entry["rating"],
            "review_count": yelp_entry["review_count"],
            "categories": yelp_entry["categories"],
        }
        i += 1
        if i % 1000 == 0:
            yelp_logger.info("Progress {}/{}".format(i, total))
            insert_response = bulk_op.execute()
            if "nUpserted" in insert_response:
                yelp_logger.debug("inserted " + str(insert_response["nUpserted"]) + " business")
            if "nModified" in insert_response:
                yelp_logger.debug("updated " + str(insert_response["nModified"]) + " business")
            bulk_op = overall.initialize_unordered_bulk_op()
        bulk_op.find({"FHRSID": yelp_entry["FHRSID"]}).upsert().update({"$set": {"yelp": add_to_overall}})
    insert_response = bulk_op.execute()
    if "nUpserted" in insert_response:
        yelp_logger.debug("inserted " + str(insert_response["nUpserted"]) + " business")
    if "nModified" in insert_response:
        yelp_logger.debug("updated " + str(insert_response["nModified"]) + " business")


if __name__ == "__main__":
    combine_yelp_to_overall()
