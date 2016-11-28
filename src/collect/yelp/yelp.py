import requests
import logging
import datetime
from pymongo import MongoClient

auth_url = "https://api.yelp.com/oauth2/token"
search_url = "https://api.yelp.com/v3/businesses/search"
review_url = "https://api.yelp.com/v3/businesses/{}/reviews"

client = MongoClient('localhost', 27017)
db = client['hygiene']
yelp = db['yelp']
yelp_reviews = db['yelp_review']

yelp.delete_many({})
yelp_reviews.delete_many({})


def get_oauth_token():
    payload = "grant_type=client_credentials&client_id=FvOr68mowlbztguJqF0spA&client_secret=BOGCjTo7zdjIQ6zUeZpZpDoI7pNNoboSYsEP5vq2YKNz4PEumQAKRbscnf6BrHCJ"
    headers = {'content-type': "application/x-www-form-urlencoded"}
    response = requests.post(auth_url, data=payload, headers=headers)
    oauth_token = response.json()['access_token']
    logger.debug("oauth_token: " + oauth_token)
    return oauth_token


def search(location):
    querystring = {
        "location": location,
        "limit": 3,
        "offset": 0
    }
    headers = {
        'authorization': "Bearer " + token
    }
    response = requests.get(search_url, headers=headers, params=querystring).json()
    total = response['total']
    logger.debug("search return " + str(total) + " total business")
    businesses = response['businesses']

    now = datetime.datetime.now()
    for business in businesses:
        business['x_create_date'] = now
    yelp.delete_many({})

    yelp.insert(businesses)
    logger.debug("inserting " + str(len(businesses)) + "  business")


def get_reviews():
    headers = {
        'authorization': "Bearer " + token
    }
    for business in yelp.find():
        response = requests.get(review_url.format(business['id']), headers=headers).json()
        reviews = response['reviews']

        now = datetime.datetime.now()
        for review in reviews:
            review['x_create_date'] = now

        logger.debug("inserting " + str(len(reviews)) + "  reviews for " + business['id'])
        yelp.insert(reviews)


def setup_logger():
    log = logging.getLogger('yelp')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)
    return log


logger = setup_logger()

token = get_oauth_token()
search("Hampshire")
get_reviews()

client.close()
