from datetime import datetime

import requests
import xmltodict
from pymongo import IndexModel, GEOSPHERE

from util import convert_to_int_and_store, setup_logger
from collect.hygiene_data.hygiene_data_links import get_hygiene_data_source
from db.connection import DbConnection


def get_southampton_restaurants_by_authorities_id(identifier):
    """
    gets all restaurants the has authorities id {id}. NOT WORKING AS API IS BROKE

    :param identifier:  local authorities id
    :return:
    """
    headers = {"x-api-version": "2", "accept": "application/json", "content-type": "application/json"}
    r = requests.get('http://api.ratings.food.gov.uk/Establishments?localAuthorityId={}'.format(identifier),
                     headers=headers)
    return r.json()


def get_authority_id(name):
    """
    pass in name of authority i.e southampton and returns the id

    :param name: City/Town
    :return: Id
    """

    headers = {"x-api-version": "2", "accept": "application/json", "content-type": "application/json"}
    r = requests.get('http://api.ratings.food.gov.uk/Authorities/basic', headers=headers)
    authorities = r.json()["authorities"]
    southampton_id = [x["LocalAuthorityId"] for x in authorities if x["Name"] == name.capitalize()]
    return southampton_id[0]


def load_data_from_xml(town="Southampton"):
    """
    Gets static data from food standards website for southampton in xml format and converts it to dict
    :return: southampton hygiene data as dict
    """
    url = get_hygiene_data_source()[town]
    hygiene_logger.debug("loading {} data: {}".format(town, url))
    r = requests.get(url)
    southampton_data = xmltodict.parse(r.text)['FHRSEstablishment']['EstablishmentCollection']["EstablishmentDetail"]
    hygiene_logger.debug("xml loaded")
    return southampton_data


def update_hygiene_data_db(data):
    """
    adds hygiene data to specified mongodb database
    :param data: dict of documents to add
    """
    hygiene_logger.debug("start inserting {} items".format(len(data)))
    hygiene_data = DbConnection().get_hygiene_collection()
    bulk_op = hygiene_data.initialize_ordered_bulk_op()
    for establishment in data:
        bulk_op.find({"FHRSID": establishment["FHRSID"]}).upsert().update({"$set": establishment})

    hygiene_logger.debug("execute bulk insert")
    insert_response = bulk_op.execute()
    if "nUpserted" in insert_response:
        hygiene_logger.debug("inserted " + str(insert_response["nUpserted"]) + " business")
    if "nModified" in insert_response:
        hygiene_logger.debug("updated " + str(insert_response["nModified"]) + " business")


def create_geo_index():
    geo_index = IndexModel([("Geocode", GEOSPHERE)])
    DbConnection().get_hygiene_collection().create_indexes([geo_index])


def clean_and_convert(data):
    clean_data = []
    hygiene_logger.debug("start cleaning")
    for establishment in data:
        if "Geocode" in establishment and establishment["Geocode"] is not None:
            establishment["Geocode"]["Longitude"] = float(establishment["Geocode"]["Longitude"])
            establishment["Geocode"]["Latitude"] = float(establishment["Geocode"]["Latitude"])
        convert_to_int_and_store(establishment, "BusinessTypeID")
        convert_to_int_and_store(establishment, "RatingValue")
        convert_to_int_and_store(establishment, "LocalAuthorityCode")
        if "RatingDate" in establishment and isinstance(establishment["RatingDate"], str):
            establishment["RatingDate"] = datetime.strptime(establishment["RatingDate"], '%Y-%m-%d')
        if "Scores" in establishment and establishment["Scores"] is not None:
            convert_to_int_and_store(establishment["Scores"], "Hygiene")
            convert_to_int_and_store(establishment["Scores"], "Structural")
            convert_to_int_and_store(establishment["Scores"], "ConfidenceInManagement")
        clean_data.append(establishment)
    return clean_data


def load_all():
    total = len(get_hygiene_data_source())
    progress = 1
    hygiene_loaded = DbConnection().get_restaurant_db().hygiene_loaded
    for key in get_hygiene_data_source().keys():
        search_key = {"name": key}
        if hygiene_loaded.count(search_key) == 0:
            hygiene_data = load_data_from_xml(key)
            update_hygiene_data_db(clean_and_convert(hygiene_data))
            hygiene_loaded.insert(search_key)
        else:
            hygiene_logger.debug("skipping {} because it was already loaded".format(key))
        hygiene_logger.info("Progress: {}/{}".format(progress, total))
        progress += 1


hygiene_logger = setup_logger("hygiene")
if __name__ == "__main__":
    load_all()
    # hygiene_data = load_data_from_xml()
    # update_hygiene_data_db(clean_and_convert(hygiene_data))
    create_geo_index()
