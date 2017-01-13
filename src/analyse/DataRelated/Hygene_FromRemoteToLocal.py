import json
from pymongo import MongoClient
from datetime import datetime


server = "svm-lw4u16-comp6235-group-6.ecs.soton.ac.uk"
port = "27018"
user = "user"
password = "banana4"
database = "restaurants"

"""
server = "svm-hf1g10-comp6235-temp.ecs.soton.ac.uk"
port = "27017"
user = "COMP6235"
password = "wkbbsdh8oDY2"
database = "health_data"

localClient = MongoClient('mongodb://127.0.0.1:27017')
dbLocal = localClient["restaurantData"]
"""
remoteClient = MongoClient('mongodb://'+user+':'+password+'@'+server+':'+port+'/'+database)
dbRemote = remoteClient["restaurants"]

for doc in dbRemote.overall.find().distinct('hygiene.LocalAuthorityName'):
    print (doc)
    break;