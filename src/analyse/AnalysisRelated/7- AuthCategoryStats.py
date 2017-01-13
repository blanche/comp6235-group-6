from pymongo import MongoClient
import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr   
import math
from operator import itemgetter
from scipy import stats
 
server = "svm-lw4u16-comp6235-group-6.ecs.soton.ac.uk"
port = "27018"
user = "user"
password = "banana4"
database = "restaurants"

remoteClient = MongoClient('mongodb://'+user+':'+password+'@'+server+':'+port+'/'+database)
dbRemote = remoteClient["restaurants"]


authList = []
for mongoDoc in dbRemote.overall.find({'hygiene':{'$exists':True}}):
    if mongoDoc['hygiene']['LocalAuthorityName'] not in authList:
        authList.append(mongoDoc['hygiene']['LocalAuthorityName'])

for auth in authList:
    restCategories = []
    for category in dbRemote.overall.find({'hygiene.LocalAuthorityName':auth}).distinct('yelp.categories'):
        restCategories.append(category)
        
    categoryCounts = []
    for restCat in restCategories:
        categoryCounts.append(dbRemote.overall.find({'hygiene.LocalAuthorityName':auth,"yelp.categories": restCat}).count())
    
    categoriyAndCount = []
    for i in range (0,len(restCategories)):
        catNCount = [restCategories[i], categoryCounts[i]]
        categoriyAndCount.append(catNCount)
        
    sortedCounts = sorted(categoriyAndCount, key=itemgetter(1),reverse=True)
    sortedCounts = sortedCounts[:6]
    
    if len(sortedCounts) > 4:
        categories = []
        categories.append(sortedCounts[0][0])
        categories.append(sortedCounts[1][0])
        categories.append(sortedCounts[2][0])
        categories.append(sortedCounts[3][0])
        categories.append(sortedCounts[4][0])
        categories.append(sortedCounts[5][0])
        
        yelpMeanList = []
        yelpMedianList = []
        cnt = 0
        for cats in categories:
            yelpRatings = []
            for mongoDoc in dbRemote.overall.find({'yelp.categories':cats ,'yelp':{'$exists':True} }):
                if mongoDoc['yelp']['rating'] > 0 and mongoDoc['yelp']['rating'] < 11: 
                    yelpRatings.append(mongoDoc['yelp']['rating'])
            try:
                mean = float("{0:.2f}".format(np.mean(yelpRatings)))
                median = float(np.median(yelpRatings))
            except:
                mean = 0
                median = 0
            yelpMeanList.append(mean)
            yelpMedianList.append(median)
        
        googleMeanList = []
        googleMedianList = []
        for cats in categories:
            googleRatings = []
            for mongoDoc in dbRemote.overall.find({'yelp.categories':cats ,'google':{'$exists':True} }):
                if mongoDoc['google']['rating'] > 0 and mongoDoc['google']['rating'] < 11: 
                    googleRatings.append(mongoDoc['google']['rating'])
            try:
                mean = float("{0:.2f}".format(np.mean(googleRatings)))
                median = float(np.median(googleRatings))
            except:
                mean = 0
                median = 0
            googleMeanList.append(mean)
            googleMedianList.append(median)
            
        hygieneMeanList = []
        hygieneMedianList = []
        for cats in categories:
            hygieneRatings = []
            for mongoDoc in dbRemote.overall.find({'yelp.categories':cats ,'hygiene':{'$exists':True} }):
                if mongoDoc['hygiene']['RatingValue'] > 0 and mongoDoc['hygiene']['RatingValue'] < 11: 
                    hygieneRatings.append(mongoDoc['hygiene']['RatingValue'])
            try:
                mean = float("{0:.2f}".format(np.mean(hygieneRatings)))
                median = float(np.median(hygieneRatings))
            except:
                mean = 0
                median = 0
            hygieneMeanList.append(mean)
            hygieneMedianList.append(median)
            
        categoryStatsArray= []
        for singleCat in categories:
            currentIndex = categories.index(singleCat)
            catStats = {
             "category":singleCat,
             "hygieneMean":hygieneMeanList[currentIndex],
             "hygieneMedian":hygieneMedianList[currentIndex],
             "yelpMean":yelpMeanList[currentIndex],
             "yelpMedian":yelpMedianList[currentIndex],
             "googleMean":googleMeanList[currentIndex],
             "googleMedian":googleMedianList[currentIndex],
            }
            categoryStatsArray.append(catStats)
        
        docToInsert = {
        "LocalAuthorityName":auth,
        "categoryResults":categoryStatsArray
        }
        
        result = dbRemote.localAuthCategory.insert_one(docToInsert) 

    if len(sortedCounts) < 4:
        categoryStatsArray= []
        for i in range (0,5):
            catStats = {
             "category":'British',
             "hygieneMean":0,
             "hygieneMedian":0,
             "yelpMean":0,
             "yelpMedian":0,
             "googleMean":0,
             "googleMedian":0,
            }
            categoryStatsArray.append(catStats)
        
        docToInsert = {
        "LocalAuthorityName":auth,
        "categoryResults":categoryStatsArray
        }
        result = dbRemote.localAuthCategory.insert_one(docToInsert) 

        