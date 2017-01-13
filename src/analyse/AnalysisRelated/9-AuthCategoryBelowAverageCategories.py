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
authList = []

for mongoDoc in dbRemote.overall.find({'hygiene':{'$exists':True}}):
    if mongoDoc['hygiene']['LocalAuthorityName'] not in authList:
        authList.append(mongoDoc['hygiene']['LocalAuthorityName'])
"""
for auth in authList:
    restCategoriesForAuth = []#Fill up different categories
    for category in dbRemote.overall.find({'hygiene.LocalAuthorityName':auth}).distinct('yelp.categories'):
        restCategoriesForAuth.append(category)
        
    avgGoogle = 0
    counter = 0
    for mongoDoc in dbRemote.overall.find({'google':{'$exists':True}, 'hygiene':{'$exists':True},'hygiene.LocalAuthorityName':auth}):
        if mongoDoc['google']['rating'] > 0 and mongoDoc['google']['rating'] < 11:
            avgGoogle = avgGoogle + mongoDoc['google']['rating']
            counter = counter + 1
    try:
        avgGoogle = float(avgGoogle) / float(counter)
    except:
        avgGoogle=0
    
    avgYelp = 0
    counter = 0
    for mongoDoc in dbRemote.overall.find({'yelp':{'$exists':True}, 'hygiene':{'$exists':True},'hygiene.LocalAuthorityName':auth}):
        if mongoDoc['yelp']['rating'] > 0 and mongoDoc['yelp']['rating'] < 11:
            avgYelp = avgYelp + mongoDoc['yelp']['rating']
            counter = counter + 1
    try:
        avgYelp = float(avgYelp) / float(counter)
    except:
        avgYelp=0
    
    avgHygiene = 0
    counter = 0
    for mongoDoc in dbRemote.overall.find({ "$or":[{'yelp':{'$exists':True}},{'google':{'$exists':True}},{'justEat':{'$exists':True}}], 'hygiene':{'$exists':True},'hygiene.LocalAuthorityName':auth}):
        if mongoDoc['hygiene']['RatingValue'] > 0 and mongoDoc['hygiene']['RatingValue'] < 11:
            avgHygiene = avgHygiene + mongoDoc['hygiene']['RatingValue']
            counter = counter + 1
    try:
        avgHygiene = float(avgHygiene) / float(counter)
    except:
        avgHygiene=0
    
    categoryLTAList = []
    for restCat in restCategoriesForAuth:
        lenRestaurants = dbRemote.overall.find({ "$or":[{'yelp':{'$exists':True}},{'google':{'$exists':True}},{'justEat':{'$exists':True}}],'hygiene':{'$exists':True},'hygiene.LocalAuthorityName':auth,'yelp.categories':restCat}).count()
        if lenRestaurants > 10:
            #Get Lower than avg occurance
            hygieneLowerThanAvgCount = 0
            googleLowerThanAvgCount = 0
            yelpLowerThanAvgCount = 0
            #Get total occurance
            hygieneTotalCnt = 0 
            yelpTotalCnt = 0
            googleTotalCnt = 0
            #Get Lower than average as percentage
            hygieneLowerThanAvg = 0.0
            googleLowerThanAvg = 0.0
            yelpLowerThanAvg = 0.0
            
            for mongoDoc in dbRemote.overall.find({'hygiene':{'$exists':True},'hygiene.LocalAuthorityName':auth,'yelp.categories':restCat  }):
                if mongoDoc['hygiene']['RatingValue'] > 0 and mongoDoc['hygiene']['RatingValue'] < avgHygiene: #Lower than avg
                    hygieneLowerThanAvgCount = hygieneLowerThanAvgCount + 1
                if mongoDoc['hygiene']['RatingValue'] > 0 and mongoDoc['hygiene']['RatingValue'] < 11: #All ratings
                    hygieneTotalCnt = hygieneTotalCnt + 1
                    
            for mongoDoc in dbRemote.overall.find({'google':{'$exists':True},'hygiene.LocalAuthorityName':auth,'yelp.categories':restCat  }):
                if mongoDoc['google']['rating'] > 0 and mongoDoc['google']['rating'] < avgGoogle:
                    googleLowerThanAvgCount = googleLowerThanAvgCount + 1
                if mongoDoc['google']['rating'] > 0 and mongoDoc['google']['rating'] < 11:
                    googleTotalCnt = googleTotalCnt + 1
                    
            for mongoDoc in dbRemote.overall.find({'yelp':{'$exists':True},'hygiene.LocalAuthorityName':auth,'yelp.categories':restCat  }):
                if mongoDoc['yelp']['rating'] > 0 and mongoDoc['yelp']['rating'] < avgYelp:
                    yelpLowerThanAvgCount = yelpLowerThanAvgCount + 1
                if mongoDoc['yelp']['rating'] > 0 and mongoDoc['yelp']['rating'] < 11:
                    yelpTotalCnt = yelpTotalCnt + 1
                
            try:
                hygieneLowerThanAvg = float(hygieneLowerThanAvgCount) / float(hygieneTotalCnt)*100
            except:
                hygieneLowerThanAvg=0
                
            try:
                googleLowerThanAvg = float(googleLowerThanAvgCount) / float(googleTotalCnt)* 100
            except:
                googleLowerThanAvg=0
                
            try:
                yelpLowerThanAvg = float(yelpLowerThanAvgCount) / float(yelpTotalCnt)* 100
            except:
                yelpLowerThanAvg=0
            
            categoryAndLTA= {
                'category':restCat,
                'hygiene':hygieneLowerThanAvg,
                'google':googleLowerThanAvg,
                'yelp':yelpLowerThanAvg
            }
            categoryLTAList.append(categoryAndLTA)
    print(auth)
    docToInsert = {
    'LocalAuthorityName':auth,
    'lowerThanAvgList':categoryLTAList
    }
    dbRemote.AuthLowerThanAvg.insert_one(docToInsert)