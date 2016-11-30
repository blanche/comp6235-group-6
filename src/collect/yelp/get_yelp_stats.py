from db.connection import DbConnection

total = DbConnection().get_yelp_collection().count()
print("Total Items: {}".format(total))

matched = DbConnection().get_yelp_collection().count({"FHRSID": {"$exists": True}})
print("Matched Items: {}".format(matched))

print("Matched Ratio: {}".format(matched/total))
