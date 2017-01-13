import json
from pymongo import MongoClient
from datetime import datetime

server = "svm-lw4u16-comp6235-group-6.ecs.soton.ac.uk"
port = "27018"
user = "user"
password = "banana4"
database = "restaurants"

remoteClient = MongoClient('mongodb://'+user+':'+password+'@'+server+':'+port+'/'+database)
dbRemote = remoteClient["restaurants"]

localClient = MongoClient('mongodb://127.0.0.1:27017')
dbLocal = localClient["restaurantData"]

for doc in dbLocal.restaurantClean.find():
    dbRemote.JustEat.insert_one(doc)