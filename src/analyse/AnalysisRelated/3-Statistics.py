from pymongo import MongoClient
import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr   
from scipy import stats
import matplotlib.pyplot as plt

server = "svm-lw4u16-comp6235-group-6.ecs.soton.ac.uk"
port = "27018"
user = "user"
password = "banana4"
database = "restaurants"

remoteClient = MongoClient('mongodb://'+user+':'+password+'@'+server+':'+port+'/'+database)
dbRemote = remoteClient["restaurants"]

gatheredAuthList = ['Southampton']
#Hygiene stats
hygieneMeanList = []
hygieneMedianList = []
hygieneModeList = []
hygieneStdevList = []

for auth in gatheredAuthList:
 hygieneRatings = []
 for mongoDoc in dbRemote.overall.find( { "$or":[{'yelp':{'$exists':True}},{'google':{'$exists':True}},{'justEat':{'$exists':True}}], 'hygiene':{'$exists':True}, 'hygiene.LocalAuthorityName':auth }):
  if mongoDoc['hygiene']['RatingValue'] > 0 and mongoDoc['hygiene']['RatingValue'] < 10: 
   hygieneRatings.append(mongoDoc['hygiene']['RatingValue'])
 mean = float("{0:.2f}".format(np.mean(hygieneRatings)))
 median = float(np.median(hygieneRatings))
 modeResult = stats.mode(hygieneRatings)
 mode = float(modeResult[0][0])
 stdev = float("{0:.2f}".format(np.std(hygieneRatings)))
 hygieneMeanList.append(mean)
 hygieneMedianList.append(median)
 hygieneModeList.append(mode)
 hygieneStdevList.append(stdev)


#Yelp stats
yelpMeanList = []
yelpMedianList = []
yelpModeList = []
yelpStdevList = []

for auth in gatheredAuthList:
 yelpRatings = []
 for mongoDoc in dbRemote.overall.find( { 'yelp':{'$exists':True}, 'hygiene':{'$exists':True}, 'hygiene.LocalAuthorityName':auth }):
  if mongoDoc['yelp']['rating'] > 0 and mongoDoc['yelp']['rating'] < 11: 
   yelpRatings.append(mongoDoc['yelp']['rating'])
 #plt.hist(yelpRatings)
 #pltVariable = 'C:\\Users\\Ut\\Desktop\\Foundations\\AutoGraphs\\'+auth+'Yelp.png'
 #plt.savefig(pltVariable)
 #plt.close()
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

 
#Google stats
googleMeanList = []
googleMedianList = []
googleModeList = []
googleStdevList = []

for auth in gatheredAuthList:
 googleRatings = []
 for mongoDoc in dbRemote.overall.find( { 'google':{'$exists':True}, 'hygiene':{'$exists':True}, 'hygiene.LocalAuthorityName':auth }):
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

"""
#UK Average Yelp
ratingList = []
for mongoDoc in dbRemote.overall.find({'yelp':{'$exists':True} }):
    if mongoDoc['yelp']['rating'] > 0 and mongoDoc['yelp']['rating'] < 11: 
        ratingList.append(mongoDoc['yelp']['rating']);
ukYelpAverage = float("{0:.2f}".format(np.mean(ratingList)))

#UK Average Google
ratingList = []
for mongoDoc in dbRemote.overall.find({'google':{'$exists':True} }):
    if mongoDoc['google']['rating'] > 0 and mongoDoc['google']['rating'] < 11: 
        ratingList.append(mongoDoc['google']['rating']);
ukGoogleAverage = float("{0:.2f}".format(np.mean(ratingList)))


#UK Hygiene Google
ratingList = []
for mongoDoc in dbRemote.overall.find({'hygiene':{'$exists':True} }):
    if mongoDoc['hygiene']['RatingValue'] > 0 and mongoDoc['hygiene']['RatingValue'] < 11: 
        ratingList.append(mongoDoc['hygiene']['RatingValue']);
ukHygieneAverage = float("{0:.2f}".format(np.mean(ratingList)))
   """     