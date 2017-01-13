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

"""
# Insert for 1,2,3
for auth in gatheredAuthList:
    currentIndex = gatheredAuthList.index(auth)
    authStats = {
         "LocalAuthorityName":auth,
         
         "hygieneMean":hygieneMeanList[currentIndex],
         "hygieneMedian":hygieneMedianList[currentIndex],
         "hygieneMode":hygieneModeList[currentIndex],
         "hygieneStdev":hygieneStdevList[currentIndex],
        
         "yelpMean":yelpMeanList[currentIndex],
         "yelpMedian":yelpMedianList[currentIndex],
         "yelpMode":yelpModeList[currentIndex],
         "yelpStdev":yelpStdevList[currentIndex],
         "yelpCorrelationHygene":gatheredYelpCorrelation[currentIndex],

         "googleMean":googleMeanList[currentIndex],
         "googleMedian":googleMedianList[currentIndex],
         "googleMode":googleModeList[currentIndex],
         "googleStdev":googleStdevList[currentIndex],
         "googleCorrelationHygene":gatheredGoogleCorrelation[currentIndex],
         
         "justEatCorrelationHygene":gatheredJustEatCorrelation[currentIndex],
    }
    result = dbRemote.localAuthStats.insert_one(authStats)
"""

# Insert for 4
for cat in categories:
    currentIndex = categories.index(cat)
    catStats = {
         "category":cat,
         
         "hygieneMean":hygieneMeanList[currentIndex],
         "hygieneMedian":hygieneMedianList[currentIndex],
         "hygieneMode":hygieneModeList[currentIndex],
         "hygieneStdev":hygieneStdevList[currentIndex],
        
         "yelpMean":yelpMeanList[currentIndex],
         "yelpMedian":yelpMedianList[currentIndex],
         "yelpMode":yelpModeList[currentIndex],
         "yelpStdev":yelpStdevList[currentIndex],
         "yelpCorrelationHygene":categoriesYelpHygieneCorr[currentIndex],

         "googleMean":googleMeanList[currentIndex],
         "googleMedian":googleMedianList[currentIndex],
         "googleMode":googleModeList[currentIndex],
         "googleStdev":googleStdevList[currentIndex],
         "googleCorrelationHygene":categoriesGoogleHygieneCorr[currentIndex],

    }
    result = dbRemote.CategoryStats.insert_one(catStats) 