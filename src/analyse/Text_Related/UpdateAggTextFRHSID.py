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
dbLocal = localClient["textDB"]


for restaurantDoc in dbRemote.overall.find({'justEat':{'$exists':True} ,'hygiene':{'$exists':True} }):
    restId = restaurantDoc['justEat']['restId']
    FHRSID = restaurantDoc['FHRSID']
    localAuth = restaurantDoc['hygiene']['LocalAuthorityName'] 
    dbLocal.aggReviews.update_one({"restId": restId},{"$set": {"LocalAuthorityName":localAuth, "FHRSID":FHRSID}})
    
