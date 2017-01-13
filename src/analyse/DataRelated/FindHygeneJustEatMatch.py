from pymongo import MongoClient 
from fuzzywuzzy import fuzz
import re

server = "svm-lw4u16-comp6235-group-6.ecs.soton.ac.uk"
port = "27018"
user = "user"
password = "banana4"
database = "restaurants"

#remoteClient = MongoClient('mongodb://'+user+':'+password+'@'+server+':'+port+'/'+database)
#dbRemote = remoteClient["restaurants"]
"""
word ="!!!AJ'Sss "
print (word)
word = re.sub('[^0-9a-zA-Z]+', '', word)
print (word)
print( fuzz.partial_ratio("AJ's", "AJs") )
"""
localClient = MongoClient('mongodb://127.0.0.1:27017')
dbLocal = localClient["restaurantData"]

cnt = 0
for justEatDoc in dbLocal.restaurantClean.find({'FHRSID':{'$exists':False}}):
    cnt = cnt+ 1
    print(cnt)
    postCode = justEatDoc['postCode']
    restName = justEatDoc['restName']
    postCode = postCode.replace(' ', '')
    postCode = postCode[:3] 
    print(postCode)
    restName = re.sub('[^0-9a-zA-Z]+', '', restName)
    queryDict = {'PostCode':{'$regex': postCode+'.*' , '$options': 'i'} }
    print(queryDict)
    for hygieneDoc in dbLocal.hygiene_data_huw.find(queryDict):
        #print (hygieneDoc['BusinessName'])
        hygieneName = hygieneDoc['BusinessName']
        hygieneName = re.sub('[^0-9a-zA-Z]+', '', hygieneName)
        
        if fuzz.partial_ratio(restName, hygieneName) > 85:
            print(restName, ' - ', hygieneName)
            dbLocal.restaurantClean.update({'_id':justEatDoc['_id']}, {"$set": {'FHRSID':hygieneDoc['FHRSID']}}, upsert=False)

print(cnt)
