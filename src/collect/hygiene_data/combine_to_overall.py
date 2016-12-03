
from src.db.connection import DbConnection
from src.util import setup_logger

hygine_logger = setup_logger("hygine")
def combine_hygiene_to_overall():
    db = DbConnection().get_restaurant_db()
    hygiene_data = db.hygiene_data.find({})
    overall = DbConnection().get_overall_collection(db)
    bulk_op = overall.initialize_ordered_bulk_op()

    for e in hygiene_data:

        FHRSID = e.pop('FHRSID', None)
        e.pop('RatingKey', None)
        e.pop('LocalAuthorityWebSite', None)
        e.pop('LocalAuthorityEmailAddress', None)
        e.pop('SchemeType', None)
        e.pop('LocalAuthorityBusinessID',None)

        bulk_op.find({"FHRSID": FHRSID}).upsert().update({"$set": {"hygiene": e}})

    insert_response = bulk_op.execute()
    if "nUpserted" in insert_response:
        hygine_logger.debug("inserted " + str(insert_response["nUpserted"]) + " business")
    if "nModified" in insert_response:
        hygine_logger.debug("updated " + str(insert_response["nModified"]) + " business")



if __name__ == "__main__":
    combine_hygiene_to_overall()
    #
    # {'BusinessType', 'Restaurant/Cafe/Canteen'
    #  'LocalAuthorityName':'Southampton',
    #  'Scores': {'Hygiene': 10, 'ConfidenceInManagement': 10, 'Structural': 10},
    #  'PostCode': 'SO17 2FW',
    #  'BusinessTypeID': 1,
    #  'LocalAuthorityCode': 877,
    # 'AddressLine2': 'Southampton',
    #  'BusinessName': '7 Bone Burger Co',
    #  'AddressLine1': '110 Portswood Road',
    #  'RatingDate': datetime.datetime(2016, 2, 16, 0, 0),
    #  'Geocode': {'Latitude': 50.922154, 'Longitude': -1.395055},
    #  'RatingValue': 3, 'NewRatingPending': 'False'
    # }