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
googleAuthList = []
for mongoDoc in dbRemote.overall.find({'google':{'$exists':True}, 'hygiene':{'$exists':True}}):
 if mongoDoc['google']['rating'] > 0 and mongoDoc['google']['rating'] < 5 and mongoDoc['hygiene']['RatingValue'] is not None:
  auth = mongoDoc['hygiene']['LocalAuthorityName']
  if auth not in googleAuthList:
   googleAuthList.append(auth)

#Add one element to keep it consistent
googleRatingPerAuth = []
hygieneRatingPerAuth = []
for i in range (0,len(googleAuthList)):
 googleRatingPerAuth.append([])
 hygieneRatingPerAuth.append([])
 
#Add ratings
for mongoDoc in dbRemote.overall.find({'google':{'$exists':True}, 'hygiene':{'$exists':True}  }):
 if mongoDoc['google']['rating'] > 0 and mongoDoc['google']['rating'] < 5 and mongoDoc['hygiene']['RatingValue'] is not None:
  #Get only records that have rating
  recordAuth = mongoDoc['hygiene']['LocalAuthorityName']
  authIndex = googleAuthList.index(recordAuth)
  hygieneRatingPerAuth[authIndex].append(mongoDoc['hygiene']['RatingValue'])
  googleRatingPerAuth[authIndex].append(mongoDoc['google']['rating']) 

hygieneGoogleCorrelation = []
for i in range (0,len(googleRatingPerAuth)):
 hygieneGoogleCorrelation.append(pearsonr(hygieneRatingPerAuth[i],googleRatingPerAuth[i])[0])