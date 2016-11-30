import bson

from src.db.connection import DbConnection
from util import setup_logger


def combine_yelp_to_overall():
    yelp_data = DbConnection.get_hygiene_collection()
    overall = DbConnection.get_overall_collection()

    logger = setup_logger("yelp")

    bulk_op = overall.initialize_ordered_bulk_op()
    for yelp_entry in yelp_data.find():
        add_to_overall = {
            "id": yelp_entry["id"],
            "price": yelp_entry["price"],
            "rating": yelp_entry["rating"],
            "review_count": yelp_entry["review_count"],
            "categories": yelp_entry["categories"],
        }
        bulk_op.find({"FHRSID": yelp_entry["FHRSID"]}).upsert().update({"$set": {"yelp": add_to_overall}})
    print(bulk_op.execute())


if __name__ == "__main__":
    combine_yelp_to_overall()
