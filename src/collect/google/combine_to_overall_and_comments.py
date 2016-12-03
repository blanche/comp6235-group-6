import bson

from src.db.connection import DbConnection
from src.util import setup_logger

# var docs = db.hygiene_data.find({})
# docs.forEach(function(doc){db.overall.insert(doc)});

google_logger = setup_logger("google")
def combine_google_found_to_overall():
    db = DbConnection().get_restaurant_db()
    google_data = db.google_reviews_found.find({})
    overall = DbConnection().get_overall_collection(db)
    bulk_op = overall.initialize_ordered_bulk_op()

    for e in google_data:
        add_to_overall = {
            "place_id": e["place_id"],
            "url": e["url"],
            "types": e["types"],
            "icon" : e["icon"],
        }

        if "rating" in e.keys():
            add_to_overall["rating"] = e["rating"]
        else:
            add_to_overall["rating"] = "NONE"

        if "permanently_closed" in e.keys():
            add_to_overall["permanently_closed"] = e["permanently_closed"]
        else:
            add_to_overall["permanently_closed"] = False

        bulk_op.find({"FHRSID": e["FHRSID"]}).upsert().update({"$set": {"google": add_to_overall}})

    insert_response = bulk_op.execute()
    if "nUpserted" in insert_response:
        google_logger.debug("inserted " + str(insert_response["nUpserted"]) + " business")
    if "nModified" in insert_response:
        google_logger.debug("updated " + str(insert_response["nModified"]) + " business")



if __name__ == "__main__":
    combine_google_found_to_overall()



    #Google
    #rating
    #reviews
    #place_id
    #website
    #types


    #Hygiene Data
    #FHRSID
    #Buisness Name
    #Postcode
    #