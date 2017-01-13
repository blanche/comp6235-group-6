from pymongo import MongoClient
import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr   
import math
 
server = "svm-lw4u16-comp6235-group-6.ecs.soton.ac.uk"
port = "27018"
user = "user"
password = "banana4"
database = "restaurants"

remoteClient = MongoClient('mongodb://'+user+':'+password+'@'+server+':'+port+'/'+database)
dbRemote = remoteClient["restaurants"]
 
#Fill auths
justEatAuthList = []
for mongoDoc in dbRemote.overall.find({'justEat':{'$exists':True}, 'hygiene':{'$exists':True}}):
 if mongoDoc['justEat']['avgRating'] > 0 and mongoDoc['justEat']['avgRating'] < 5 and mongoDoc['hygiene']['RatingValue'] is not None:
  auth = mongoDoc['hygiene']['LocalAuthorityName']
  if auth not in justEatAuthList:
   justEatAuthList.append(auth)

#Add one element to keep it consistent
justEatRatingPerAuth = []
hygieneRatingPerAuth = []
for i in range (0,len(justEatAuthList)):
 justEatRatingPerAuth.append([])
 hygieneRatingPerAuth.append([])
 
#Add ratings
for mongoDoc in dbRemote.overall.find({'justEat':{'$exists':True}, 'hygiene':{'$exists':True}  }):
 if mongoDoc['justEat']['avgRating'] > 0 and mongoDoc['justEat']['avgRating'] < 5 and mongoDoc['hygiene']['RatingValue'] is not None:
  #Get only records that have rating
  recordAuth = mongoDoc['hygiene']['LocalAuthorityName']
  authIndex = justEatAuthList.index(recordAuth)
  hygieneRatingPerAuth[authIndex].append(mongoDoc['hygiene']['RatingValue'])
  justEatRatingPerAuth[authIndex].append(mongoDoc['justEat']['avgRating']) 

hygieneJustEatCorrelation = []
for i in range (0,len(justEatRatingPerAuth)):
 if not math.isnan(pearsonr(hygieneRatingPerAuth[i],justEatRatingPerAuth[i])[0]):
  hygieneJustEatCorrelation.append(pearsonr(hygieneRatingPerAuth[i],justEatRatingPerAuth[i])[0])

