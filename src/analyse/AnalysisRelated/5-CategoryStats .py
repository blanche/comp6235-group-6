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

"""
restCategories = []
for category in dbRemote.overall.find().distinct('yelp.categories'):
    restCategories.append(category)
    
categoryCounts = []
for restCat in restCategories:
    categoryCounts.append(dbRemote.overall.find({"yelp.categories": restCat}).count())

categoriyAndCount = []
for i in range (0,len(restCategories)):
    catNCount = [restCategories[i], categoryCounts[i]]
    categoriyAndCount.append(catNCount)
    
sortedCounts = sorted(categoriyAndCount, key=itemgetter(1))
sortedCounts = sortedCounts[-20:]
"""

categories = ['Pubs','Fast Food','British','Indian','Italian','Chinese','Pakistani','Fish & Chips','Cafes','Hotels']
"""
for item in sortedCounts:
    categories.append(item[0])
"""

"""
yelpMeanList = []
yelpMedianList = []
yelpModeList = []
yelpStdevList = []

cnt = 0
for cats in categories:
    yelpRatings = []
    for mongoDoc in dbRemote.overall.find({'yelp.categories':cats ,'yelp':{'$exists':True} }):
        if mongoDoc['yelp']['rating'] > 0 and mongoDoc['yelp']['rating'] < 11: 
            yelpRatings.append(mongoDoc['yelp']['rating'])
    try:
        mean = float("{0:.2f}".format(np.mean(yelpRatings)))
        median = float(np.median(yelpRatings))
        modeResult = stats.mode(yelpRatings)
        mode = float(modeResult[0][0])
        stdev = float("{0:.2f}".format(np.std(yelpRatings)))
    except:
        mean = 0
        median = 0
        mode = 0
        stdev = 0
    yelpMeanList.append(mean)
    yelpMedianList.append(median)
    yelpModeList.append(mode)
    yelpStdevList.append(stdev)

googleMeanList = []
googleMedianList = []
googleModeList = []
googleStdevList = []
    
for cats in categories:
    googleRatings = []
    for mongoDoc in dbRemote.overall.find({'yelp.categories':cats ,'google':{'$exists':True} }):
        if mongoDoc['google']['rating'] > 0 and mongoDoc['google']['rating'] < 11: 
            googleRatings.append(mongoDoc['google']['rating'])
    try:
        mean = float("{0:.2f}".format(np.mean(googleRatings)))
        median = float(np.median(googleRatings))
        modeResult = stats.mode(googleRatings)
        mode = float(modeResult[0][0])
        stdev = float("{0:.2f}".format(np.std(googleRatings)))
    except:
        mean = 0
        median = 0
        mode = 0
        stdev = 0
    googleMeanList.append(mean)
    googleMedianList.append(median)
    googleModeList.append(mode)
    googleStdevList.append(stdev)
    
hygieneMeanList = []
hygieneMedianList = []
hygieneModeList = []
hygieneStdevList = []
    
for cats in categories:
    hygieneRatings = []
    for mongoDoc in dbRemote.overall.find({'yelp.categories':cats ,'hygiene':{'$exists':True} }):
        if mongoDoc['hygiene']['RatingValue'] > 0 and mongoDoc['hygiene']['RatingValue'] < 11: 
            hygieneRatings.append(mongoDoc['hygiene']['RatingValue'])
    try:
        mean = float("{0:.2f}".format(np.mean(hygieneRatings)))
        median = float(np.median(hygieneRatings))
        modeResult = stats.mode(hygieneRatings)
        mode = float(modeResult[0][0])
        stdev = float("{0:.2f}".format(np.std(hygieneRatings)))
    except:
        mean = 0
        median = 0
        mode = 0
        stdev = 0
    hygieneMeanList.append(mean)
    hygieneMedianList.append(median)
    hygieneModeList.append(mode)
    hygieneStdevList.append(stdev)
    
# Stats end, correlation calculation begins

categoriesGoogleHygieneCorr = []
for cats in categories:
    googleRatings = []
    hygieneRatings = []
    for mongoDoc in dbRemote.overall.find({'yelp.categories':cats ,'google':{'$exists':True},'hygiene':{'$exists':True} }):
         if mongoDoc['google']['rating'] > 0 and mongoDoc['google']['rating'] < 5 and mongoDoc['hygiene']['RatingValue'] is not None:
             googleRatings.append(mongoDoc['google']['rating'])
             hygieneRatings.append(mongoDoc['hygiene']['RatingValue'])
    categoriesGoogleHygieneCorr.append(pearsonr(googleRatings,hygieneRatings)[0])
        
categoriesYelpHygieneCorr = []
for cats in categories:
    yelpRatings = []
    hygieneRatings = []
    for mongoDoc in dbRemote.overall.find({'yelp.categories':cats ,'yelp':{'$exists':True},'hygiene':{'$exists':True} }):
         if mongoDoc['yelp']['rating'] > 0 and mongoDoc['yelp']['rating'] < 5 and mongoDoc['hygiene']['RatingValue'] is not None:
             yelpRatings.append(mongoDoc['yelp']['rating'])
             hygieneRatings.append(mongoDoc['hygiene']['RatingValue'])
    categoriesYelpHygieneCorr.append(pearsonr(yelpRatings,hygieneRatings)[0])      
        
"""
#UK Average