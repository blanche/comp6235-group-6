import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from pymongo import MongoClient 


def countWords (wordList):
    countedWordsDict = {}
    for i in range (0,len(wordList)):
        currentWord = wordList[i]
        if countedWordsDict.get(currentWord) == None:
            dictToAdd = {currentWord:1}
            countedWordsDict.update(dictToAdd)
        else:
            singleWordCount = countedWordsDict.get(currentWord)
            countedWordsDict.update({currentWord:singleWordCount+1})
    return countedWordsDict
    
def FillPositiveNegativeList():
    positiveWords = []
    negativeWords = []
    with open('C:\Users\Ut\Desktop\Foundations\positive.txt', 'r') as readFile:
        for line in readFile:
            line = line.replace('\n','')
            positiveWords.append(line)
            
    with open(r'C:\Users\Ut\Desktop\Foundations\negative.txt', 'r') as readFile:
        for line in readFile:
            line = line.replace('\n','')
            negativeWords.append(line)
    adjectiveList = positiveWords  +  negativeWords
    return adjectiveList
    


adjectiveList=FillPositiveNegativeList()

localClient = MongoClient('mongodb://127.0.0.1:27017')
dbLocal = localClient["textDB"]

restList = dbLocal.gatheredTexts.find({},{"restId":1}).distinct("restId")
existingRestaurants = dbLocal.aggReviews.find({},{"restId":1}).distinct("restId")
restList = [x for x in restList if x not in existingRestaurants]

cnt = 0
restAdjectives = []
restVerbs = []
restNouns = []

adjDict = {}
verbDict = {}
nounDict = {}

restIdOld = ''
for restId in restList:
    #try:
    print(restId)
    for textDoc in dbLocal.gatheredTexts.find({"restId":restId}):
        try:
            sentence = str(textDoc['Comment'])
            sentence = sentence.lower()
            sentence = re.sub('[^0-9a-zA-Z \']+', '', sentence)
            stop_words = set(stopwords.words('english'))#where, from etc...
            word_tokens = nltk.word_tokenize(sentence)#Tokenize the sentence
            
            filtered_sentence = [w for w in word_tokens if not w in stop_words]#Clean stuff
                
            tagged = nltk.pos_tag(filtered_sentence)
            
            lemmatizer = WordNetLemmatizer() 
            for i in range (0,len(tagged)):
                word = tagged[i][0]
                type = tagged[i][1]
                if ( type in ('JJ','JJR','JJS')):#Normal adj, second form, third form
                    if(word =='best'):
                        word = 'good'
                    restAdjectives.append(lemmatizer.lemmatize(word, pos="a"))
                if ( type in ('NN','NNP','NNPS','NNS')):#Nouns
                    restNouns.append(lemmatizer.lemmatize(word))
                if ( type in ('VB','VBD','VBG','VBN','VBP','VBZ')):#Nouns
                    restVerbs.append(lemmatizer.lemmatize(word, pos="v")) 
        except:
            print('Ex for one sentence')
    adjDict = countWords(restAdjectives)
    adjDict = sorted(adjDict.items(), key=lambda x: x[-1])
    adjListTop20 = list(adjDict)[-30:]
    
    verbDict = countWords(restVerbs)
    nounDict = countWords(restNouns)
    
    #Clean adjectives
    for item in adjListTop20:
        word = item[0]
        count = item[1]
        if str(word) not in adjectiveList:
            if (word[-2:] != 'ty'): 
                if verbDict.get(word) != None:
                    verbDict.update({word:count + verbDict.get(word)}) 
                if nounDict.get(word) != None:
                    nounDict.update({word:count + nounDict.get(word)})
                adjListTop20.remove(item)
    
    verbDict = sorted(verbDict.items(), key=lambda x: x[-1])
    nounDict = sorted(nounDict.items(), key=lambda x: x[-1])
    verbListTop20 = list(verbDict)[-20:]
    nounListTop20 = list(nounDict)[-20:]
    
    singleRestaurantReviews = {
        "restId":restIdOld,
        "adjList": adjListTop20,
        "verbList":verbListTop20,
        "nounList":nounListTop20
    }
    result = dbLocal.aggReviews.insert_one(singleRestaurantReviews)
    #print(singleRestaurantReviews)
    #Empty list
    restAdjectives = []
    restVerbs = []
    restNouns = []
    restIdOld = restId
    #except:
    #    print('Ex')