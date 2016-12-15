from db.connection import DbConnection

total = DbConnection().get_yelp_collection().count()
print("Total Items: {}".format(total))

matched = DbConnection().get_yelp_collection().count({"FHRSID": {"$exists": True}})
print("Matched Items: {}".format(matched))

print("Matched Ratio: {}".format(matched/total))


yelp_in_overall = DbConnection().get_overall_collection().count({"yelp": {"$exists": True}})
print("Yelp in Overall: {}".format(yelp_in_overall))
overall_count = DbConnection().get_overall_collection().count()
print("Total in Overall: {}".format(overall_count))
