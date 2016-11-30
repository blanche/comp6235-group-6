import time
from difflib import SequenceMatcher

import bson
import requests

from src.db.connection import DbConnection

API_KEY = "AIzaSyCp44cd14BYXibwjShWTltAQEosC0tfU-A"
s = requests.Session()

def similar(a, b):
    """
    Compares two strings and returns decimal. high similar, low not similar

    :param a: String One
    :param b: String Two
    :return: Decimal
    """
    return SequenceMatcher(None, a, b).ratio()


# lat, long
def get_place_by_name_and_address(establishment):
    """Returns list off all places found matching set criteria with google id of place in results

    Criteria:
        type : e.g Pub
        location: lat , long
        keyword : e.g nandos
        radius : e.g 10 (in meters from specified location

        :return: List
    """
    if(establishment["Geocode"] is None or establishment["BusinessName"] is None):
        print("No Name of GeoCode in {}".format(establishment))
        establishment["reason"] = "No Geocode or Name"
        establishment["GoogleSearchUrl"] = "No Geocode or Name"
        return []
    url =  "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}0&keyword={name}&type={type}&radius=300&key={key}".format(
            lat=establishment["Geocode"]["Latitude"],
            long=establishment["Geocode"]["Longitude"],
            name=establishment["BusinessName"].replace(" ", "%20").replace("'","%27") + "%20" + establishment['LocalAuthorityName'],
            type=establishment["BusinessType"].replace(" ", "%20").replace("'","%27"),
            key=API_KEY)
    establishment["GoogleSearchUrl"] = url
    r = s.get(url)
    data = r.json()
    if len(data["results"]) == 0:
        establishment["reason"] = "No google search results found for {}".format(establishment["BusinessName"])
        print("No google search results found for {}".format(establishment["BusinessName"]))
    return data["results"]


def _get_place_details_by_id(place_id):
    r = s.get(
        "https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}".format(place_id, API_KEY))
    data = r.json()
    return data


def get_place_details_if_similar(google_data_list, establishment_hygiene):

    """
        Compares names found in google_data_list to hygiene place name. If similar returns match else None

        :param google_data_list:
        :param hygiene_place_name: name of establishment from hygiene data
        :return: Most similar place or None

    """

    def from_returned_data_get_most_likely_match():
        """

        :return: tuple: (str:placeName, int:match rating)
        """
        hygiene_place_name = establishment_hygiene["BusinessName"]
        print("{} vs {}".format(hygiene_place_name, [x["name"] for x in google_data_list]))
        most_likely_place = max([(place, similar(place["name"], hygiene_place_name)) for place in google_data_list],
                                key=lambda x: x[1])
        return most_likely_place



    most_likely_place = from_returned_data_get_most_likely_match()
    hygiene_place_name = establishment_hygiene["BusinessName"]

    #Place has similarity rating above 0.5 or name within hygiene name
    if most_likely_place[1] > 0.5 or hygiene_place_name in most_likely_place[0]["name"]:
        most_likely_place_id = most_likely_place[0]["place_id"]
        print("Gone with {}".format(most_likely_place[0]["name"]))
        place_details = _get_place_details_by_id(most_likely_place_id)
        return place_details["result"]
    else:

        #If not similar check for a results returned and check of name within name
        one_contains_other = [x for x in google_data_list
                              if x["name"].strip().lower() in hygiene_place_name.strip().lower() or
                              hygiene_place_name.strip().lower() in x["name"].strip().lower()]
        if len(one_contains_other) == 1:
            print("Gone with {}".format(one_contains_other[0]["name"]))
            place_details = _get_place_details_by_id(one_contains_other[0]["place_id"])
            return place_details["result"]
        else:
            # Produce reason why didn't match
            reason = "google found: {} none match search name : {}, Not close enough to add".format(
                [x["name"] for x in google_data_list], hygiene_place_name)
            establishment_hygiene["Reason"] = reason
            print(establishment_hygiene["Reason"])
            return None


def add_data_to_google_found(db, data):
    for found_data in data:
        key = bson.son.SON({"FHRSID": found_data["FHRSID"]})
        data = bson.son.SON(found_data)
        db.google_reviews_found.update(key, data, upsert=True)


def add_data_to_google_not_found(db, data):
    for not_found_data in data:
        key = bson.son.SON({"FHRSID": not_found_data["FHRSID"]})
        data = bson.son.SON(not_found_data)
        db.google_reviews_not_found.update(key, data, upsert=True)


def get_google_places_for_current_of_higene_data_establishments():
    # DB
    not_found_list = []
    found_list = []
    db = DbConnection().get_restaurant_db()
    establishments = [est for est in db.hygiene_data.find()]
    establishments = establishments
    for e in establishments:
        time.sleep(0.75) # sleep to stop api cutting out for requests per second
        print(establishments.index(e))
        google_find_data = get_place_by_name_and_address(e)
        if len(google_find_data) != 0:
            place = get_place_details_if_similar(google_find_data, e)
            if(place):
                place["FHRSID"] = e["FHRSID"]
                found_list.append(place)
            else:
                not_found_list.append(e)
        else:
            e["Reason"] = "Not Results returned In Google Search api"
            not_found_list.append(e)

    add_data_to_google_found(db, found_list)
    add_data_to_google_not_found(db, not_found_list)


if __name__ == "__main__":
    get_google_places_for_current_of_higene_data_establishments()
    db = DbConnection().get_restaurant_db()
    [print(x["BusinessName"], x["Reason"], x["GoogleSearchUrl"]) for x in db.google_reviews_not_found.find()]
