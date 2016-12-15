import datetime
import difflib
import time
import requests
from pymongo import IndexModel, GEOSPHERE

from util import setup_logger, restaurant_stopwords, name_clean_re
from db.connection import DbConnection


def get_oauth_token():
    payload = "grant_type=client_credentials&client_id=FvOr68mowlbztguJqF0spA&client_secret=BOGCjTo7zdjIQ6zUeZpZpDoI7pNNoboSYsEP5vq2YKNz4PEumQAKRbscnf6BrHCJ"
    headers = {'content-type': "application/x-www-form-urlencoded"}
    response = requests.post(auth_url, data=payload, headers=headers)
    oauth_token = response.json()['access_token']
    yelp_logger.debug("oauth_token: " + oauth_token)
    return oauth_token


def search_by_location(location):
    headers = {
        'authorization': "Bearer " + token
    }
    total = 99999
    page_size = 50  # maximum limit for api is 50
    current_offset = 0

    yelp_logger.debug("loading {} from yelp".format(location))
    bulk_op = yelp_data.initialize_unordered_bulk_op()
    now = datetime.datetime.now()
    ops = 0
    while total > current_offset:
        querystring = {
            "location": location,
            "limit": page_size,
            "offset": current_offset
        }
        r = requests.get(search_url, headers=headers, params=querystring)

        if r.status_code == 200:
            response = r.json()
            total = response['total']
            # if total > 1000:
            #     yelp_logger.error("REFINE {}:{}".format(location, total))
            #     return False

            for business in response['businesses']:
                business['x_create_date'] = now
                clean(business)
                bulk_op.find({"id": business["id"]}).upsert().update_one({"$set": business})
                ops += 1

            current_offset += page_size
            if current_offset > 999:
                yelp_logger.warn("SKIPPING {} entries in {}".format(total - 1000, location))
                break
            yelp_logger.debug("Progress {}/{}".format(current_offset, total))
        else:
            yelp_logger.error(r)
            return False

    yelp_logger.debug("search return " + str(total) + " total business")
    if ops > 0:
        yelp_logger.debug("executing bulk update")
        insert_response = bulk_op.execute()

        yelp_logger.debug("inserted " + str(insert_response["nUpserted"]) + "  business")
        yelp_logger.debug("updated " + str(insert_response["nModified"]) + "  business")
    return True


def clean(business):
    if "price" in business:
        business['price'] = len(business['price']) * 1.25  # normalize to 1-5
    else:
        business['price'] = None

    if "categories" in business and isinstance(business["categories"], list):
        clean_category = []
        for category in business["categories"]:
            clean_category.append(category["title"])
        business["categories"] = clean_category


def get_reviews():
    headers = {
        'authorization': "Bearer " + token
    }

    for business in yelp_data.find():
        response = requests.get(review_url.format(business['id']), headers=headers).json()
        reviews = response['reviews']

        now = datetime.datetime.now()
        for review in reviews:
            review['x_create_date'] = now

        yelp_logger.debug("inserting " + str(len(reviews)) + "  reviews for " + business['id'])
        yelp_data.insert(reviews)


def match_yelp_with_hygiene_data():
    bulk_op = yelp_data.initialize_unordered_bulk_op()

    totaltotal = DbConnection().get_yelp_collection().count({"matched": {"$exists": False}})
    matched = 0.0
    matched_total = 0.0
    total = 0.0
    # for y in yelp_data.find({"FHRSID": {"$exists": False}}).sort({"_id":-1}):
    for y in yelp_data.find({"matched": {"$exists": False}}).sort("_id", 1):
        total += 1
        if y["coordinates"]["latitude"] is None:
            continue
        update = False
        yelp_name = clean_name(y["name"])
        closest = [0, None]
        for h in hygiene_data.find(
                {"Geocode":
                     {"$near":
                          {"$geometry":
                               {"type": "Point",
                                "coordinates": [y["coordinates"]["longitude"], y["coordinates"]["latitude"]]
                                }
                           }
                      }
                 }).limit(30):
            business_name = clean_name(h["BusinessName"])
            ratio = difflib.SequenceMatcher(lambda x: x == " ", yelp_name, business_name).ratio()
            # yelp_logger.debug(business_name)
            if ratio > closest[0]:
                closest = [ratio, h]
        if closest[0] > 0.9:
            # yelp_logger.debug("LEVEN: " + y["name"] + "-" + closest[1]["BusinessName"])
            update = True
        else:
            if closest[1] is not None:
                hygiene_name = clean_name(closest[1]["BusinessName"])
                if yelp_name in hygiene_name or hygiene_name in yelp_name:
                    # yelp_logger.debug("SUBSTR: " + y["name"] + "-" + closest[1]["BusinessName"])
                    update = True
                    # elif closest[0] > 0.5:
                    # yelp_logger.debug("MAYBE " + yelp_name + " = " + hygiene_name + " - " + str(closest[0]))
                    # else:
                    #     print("NO " + yelp_name + " = " + hygiene_name + " - " + str(closest[0]))
        if update:
            matched += 1
            bulk_op.find({"id": y["id"]}).update({"$set": {"FHRSID": closest[1]['FHRSID'], "matched": True}})
        else:
            bulk_op.find({"id": y["id"]}).update({"$set": {"matched": True}})
        if matched > 0 and matched % 1000 == 0:
            yelp_logger.debug("executing bulk update")
            bulk_op.execute()
            bulk_op = yelp_data.initialize_unordered_bulk_op()
            matched_total += matched
            matched = 0
        if total % 100 == 0:
            yelp_logger.debug("Progress {}/{}/{}".format(matched, total, totaltotal))
    yelp_logger.info("Matching rate: " + str(float(matched_total) / total))
    yelp_logger.debug("executing bulk update")
    bulk_op.execute()


def clean_name(name):
    name = name_clean_re.sub('', name.lower()).strip()
    return " ".join([word for word in name.split() if word.lower() not in restaurant_stopwords])


def create_geo_index():
    geo_index = IndexModel([("coordinates", GEOSPHERE)])
    yelp_data.create_indexes([geo_index])


def load_all():
    # with open("postcodes.txt") as f:
    with open("postcode4_refine.txt") as f:
        content = f.readlines()
    # content.reverse()
    progress = 1
    refine = []
    # remove already parsed post codes
    # del content[:1960]

    total = len(content)
    yelp_loaded = DbConnection().get_restaurant_db().yelp_loaded
    for key in content:
        key = key.strip()
        search_key = {"name": key}
        if yelp_loaded.count(search_key) == 0:
            done = search_by_location(key)
            if not done:
                refine.append(key)
            else:
                yelp_loaded.insert(search_key)
        else:
            yelp_logger.debug("skipping {} because it was already loaded".format(key))
        yelp_logger.info("Progress: {}/{}".format(progress, total))
        progress += 1
    yelp_logger.warn(refine)


yelp_logger = setup_logger("yelp")

if __name__ == "__main__":
    auth_url = "https://api.yelp.com/oauth2/token"
    search_url = "https://api.yelp.com/v3/businesses/search"
    review_url = "https://api.yelp.com/v3/businesses/{}/reviews"

    con = DbConnection()
    db = con.get_restaurant_db()
    yelp_data = con.get_yelp_collection(db)
    yelp_review_data = db['yelp_review_data']
    hygiene_data = con.get_hygiene_collection(db)

    # token = get_oauth_token()
    # load_all()
    # search_by_location("Southampton")
    # create_geo_index()
    match_yelp_with_hygiene_data()
    # get_reviews()
