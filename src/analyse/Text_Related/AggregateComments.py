from pymongo import MongoClient 
from fuzzywuzzy import fuzz
import re
from operator import itemgetter

def AggregateList(listOne,listTwo):
    listToReturn = []
    addedElementsIndex = []
    for wordNCountOne in listOne:
        wordOne = wordNCountOne[0]
        countOne = wordNCountOne[1]
        wordMatchNotFound = True
        wordToAdd = []
        for wordNCountTwo in listTwo:
            wordTwo = wordNCountTwo[0]
            countTwo = wordNCountTwo[1]
            if wordOne == wordTwo:
                indexTwo = listTwo.index(wordNCountTwo)
                addedElementsIndex.append(indexTwo)
                wordMatchNotFound = False
                wordToAdd = [wordOne, (int(countOne)+int(countTwo))]
                listToReturn.append(wordToAdd)
        if wordMatchNotFound:
            listToReturn.append([wordOne, countOne])
    
    for wordNCountTwo in listTwo:
        index = listTwo.index(wordNCountTwo)
        if index not in addedElementsIndex:
            listToReturn.append(wordNCountTwo)
    return listToReturn
   
def CleanList(listOne, topNPercentage):
    listToReturn = []
    lowerBound = len(listOne)-1 - len(listOne)*topNPercentage/100
    for i in range(lowerBound,len(listOne)):
        listToReturn.append(listOne[i])
    return listToReturn
    
                         
                         
"""
server = "svm-lw4u16-comp6235-group-6.ecs.soton.ac.uk"
port = "27018"
user = "user"
password = "banana4"
database = "restaurants"

#remoteClient = MongoClient('mongodb://'+user+':'+password+'@'+server+':'+port+'/'+database)
#dbRemote = remoteClient["restaurants"]
"""

localClient = MongoClient('mongodb://127.0.0.1:27017')
dbLocal = localClient["textDB"]

localAuthList = []
for localAuth in dbLocal.aggReviews.find().distinct('LocalAuthorityName'):#Change this with local auth 
    localAuthList.append(localAuth)#Got a list full of local auths

for auth in localAuthList:#For each local auth 
    adjAggregated = [['good',1]]
    verbAggreagated = [['deliver',1]]
    nounAggregated = [['food',1]]
    for singleDocument in dbLocal.aggReviews.find({'LocalAuthorityName':auth}):#Query to get all that auths data
        adj = singleDocument['adjList']
        verb = singleDocument['verbList']
        noun = singleDocument['nounList'] # Got all lists
        adjAggregated= AggregateList(adjAggregated,adj)  
        verbAggreagated= AggregateList(verbAggreagated,verb)
        nounAggregated= AggregateList(nounAggregated,noun)
        
        adjAggregated = sorted(adjAggregated, key=itemgetter(1))
        verbAggreagated= sorted(verbAggreagated, key=itemgetter(1))
        nounAggregated= sorted(nounAggregated, key=itemgetter(1))
        
        adjAggregated = CleanList(adjAggregated,40)
        verbAggreagated = CleanList(verbAggreagated,40)
        nounAggregated = CleanList(nounAggregated,40)
         
    aggregatedComments = {
        "LocalAuthorityName":auth,
        "adjList": adjAggregated,
        "verbList":verbAggreagated,
        "nounList":nounAggregated
    }
    result = dbLocal.cityAggReviewsClean.insert_one(aggregatedComments)
    
"""
for restaurantDoc in dbRemote.overall.find({'justEat':{'$exists':True}}):
    restIds = restaurantDoc['justEat']['restId']
    FHRSID = restaurantDoc['FHRSID']
    localAuth = restaurantDoc['hygiene']['LocalAuthorityName'] 

    dbLocal.aggReviews.update_one({"restId": restIds},{"$set": {"LocalAuthorityName":localAuth, "FHRSID":FHRSID}})
"""

x 
            
            