from pymongo import MongoClient 
from fuzzywuzzy import fuzz
import re

server = "svm-lw4u16-comp6235-group-6.ecs.soton.ac.uk"
port = "27018"
user = "user"
password = "banana4"
database = "restaurants"

remoteClient = MongoClient('mongodb://'+user+':'+password+'@'+server+':'+port+'/'+database)
dbRemote = remoteClient["restaurants"]
 
localClient = MongoClient('mongodb://127.0.0.1:27017')
dbLocal = localClient["restaurantData"]

updatedCnt = 0
insertedCnt = 0
for justEatDoc in dbLocal.restaurantClean.find({'FHRSID':{'$exists':True}}):
    fhrsid = justEatDoc['FHRSID'] 
    city = justEatDoc['city']
    restId = justEatDoc['restId']
    restName = justEatDoc['restName']
    avgRating = justEatDoc['avgRating']
    foodQualityRating = justEatDoc['foodQualityRating']
    deliveryRating = justEatDoc['deliveryRating']
    serviceRating = justEatDoc['serviceRating']
    totalReviews = justEatDoc['totalReviews']
 
    recordExists = dbRemote.overall.find({"FHRSID":fhrsid})
    """
    if (recordExists.count() == 0):
        insertedCnt = insertedCnt + 1
        result = dbRemote.overall.insert_one({
         "FHRSID":fhrsid,
         "justEat":{
             "restId":restId,
             "restName":restName,
             "city":city,
             "avgRating":avgRating,
             "deliveryRating":deliveryRating,
             "serviceRating":serviceRating,
             "totalReviews":totalReviews    
             }
         })
    """
    if (recordExists.count() ==1 ):
        updatedCnt = updatedCnt + 1
        justEatData = {
            "restId":restId,
             "restName":restName,
             "city":city,
             "avgRating":avgRating,
             "deliveryRating":deliveryRating,
             "serviceRating":serviceRating,
             "totalReviews":totalReviews,
             "foodQualityRating":foodQualityRating
        }
        result = dbRemote.overall.update_one({"FHRSID": fhrsid},{"$set": {"justEat":justEatData}})
        print("ok")
print(updatedCnt)
print(insertedCnt)
