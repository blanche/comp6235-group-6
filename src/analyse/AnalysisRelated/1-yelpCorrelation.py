from pymongo import MongoClient
import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr   
 
server = "svm-lw4u16-comp6235-group-6.ecs.soton.ac.uk"
port = "27018"
user = "user"
password = "banana4"
database = "restaurants"

remoteClient = MongoClient('mongodb://'+user+':'+password+'@'+server+':'+port+'/'+database)
dbRemote = remoteClient["restaurants"]
 
#Fill auths
yelpAuthList = []
for mongoDoc in dbRemote.overall.find({'yelp':{'$exists':True}, 'hygiene':{'$exists':True}}):
 if mongoDoc['yelp']['rating'] > 0 and mongoDoc['yelp']['rating'] < 5 and mongoDoc['hygiene']['RatingValue'] is not None:
  auth = mongoDoc['hygiene']['LocalAuthorityName']
  if auth not in yelpAuthList:
   yelpAuthList.append(auth)

#Add one element to keep it consistent
yelpRatingPerAuth = []
hygieneRatingPerAuth = []
for i in range (0,len(yelpAuthList)):
 yelpRatingPerAuth.append([])
 hygieneRatingPerAuth.append([])
 
#Add ratings
for mongoDoc in dbRemote.overall.find({'yelp':{'$exists':True}, 'hygiene':{'$exists':True}  }):
 if mongoDoc['yelp']['rating'] > 0 and mongoDoc['yelp']['rating'] < 5:
  #Get only records that have rating
  recordAuth = mongoDoc['hygiene']['LocalAuthorityName']
  authIndex = yelpAuthList.index(recordAuth)
  hygieneRatingPerAuth[authIndex].append(mongoDoc['hygiene']['RatingValue'])
  yelpRatingPerAuth[authIndex].append(mongoDoc['yelp']['rating']) 

hygieneYelpCorrelation = []
for i in range (0,len(yelpRatingPerAuth)):
 hygieneYelpCorrelation.append(pearsonr(hygieneRatingPerAuth[i],yelpRatingPerAuth[i])[0])

