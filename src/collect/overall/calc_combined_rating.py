from db.connection import DbConnection

from util import setup_logger

overall_collection = DbConnection().get_overall_collection()
overall_logger = setup_logger("overall")

i = 0
bulk_op = overall_collection.initialize_unordered_bulk_op()
for o in overall_collection.find(
        {"$or": [{"yelp": {"$exists": True}}, {"google": {"$exists": True}}, {"justEat": {"$exists": True}}]}):
    combined_rating = []
    if 'rating' in o and "rating" in o['rating']:
        combined_rating.append(o['rating']['rating'])
    if 'yelp' in o and "rating" in o['yelp']:
        combined_rating.append(o['yelp']['rating'])
    if 'justEat' in o and "avgRating" in o['justEat']:
        combined_rating.append(o['justEat']['avgRating'])
    if len(combined_rating) > 0:
        rating = sum(combined_rating) / float(len(combined_rating))
        bulk_op.find({"_id": o["_id"]}).update(
            {"$set": {"combined_rating": rating}})
        i += 1
    if i >= 1000:
        insert_response = bulk_op.execute()
        overall_logger.debug("updated " + str(insert_response["nModified"]) + " entries")
        bulk_op = overall_collection.initialize_unordered_bulk_op()
        i = 0

overall_logger.info("last insert")
insert_response = bulk_op.execute()
overall_logger.debug("updated " + str(insert_response["nModified"]) + " entries")
