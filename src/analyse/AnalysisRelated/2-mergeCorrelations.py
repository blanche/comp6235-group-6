#hygieneYelpCorrelation
#hygieneGoogleCorrelation
#googleAuthList
#yelpAuthList

gatheredAuthList = []
gatheredYelpCorrelation = []
gatheredGoogleCorrelation = []
gatheredJustEatCorrelation = []

#Append google and yelp uths
for auth in googleAuthList:
 if auth not in gatheredAuthList:
  gatheredAuthList.append(auth)
  
for auth in yelpAuthList:
 if auth not in gatheredAuthList:
  gatheredAuthList.append(auth)
  
for auth in justEatAuthList:
 if auth not in gatheredAuthList:
  gatheredAuthList.append(auth)

#Append zeros to be able to change them and not get index error
for records in gatheredAuthList:
 gatheredYelpCorrelation.append(0)
 gatheredGoogleCorrelation.append(0)
 gatheredJustEatCorrelation.append(0)
 
for auth in gatheredAuthList:
 currentIndex = gatheredAuthList.index(auth)
 try:
  yIndex = yelpAuthList.index(auth)
  gatheredYelpCorrelation[currentIndex] = hygieneYelpCorrelation[yIndex]
 except:
  x=1
  
 try:
  gIndex = googleAuthList.index(auth)
  gatheredGoogleCorrelation[currentIndex] = hygieneGoogleCorrelation[gIndex]
 except:
  x=5
  
 try:
  jIndex = justEatAuthList.index(auth)
  gatheredJustEatCorrelation[currentIndex] = hygieneJustEatCorrelation[jIndex]
 except:
  x=5