import bson
import requests
import xmltodict

from src.db.connection import DbConnection
from src.collect.hygiene_data.hygiene_data_links import get_hygiene_data_source


def get_southampton_restaurants_by_authorities_id(identifier):
    """
    gets all restaurants the has authorites id {id}. NOT WORKING AS API IS BROKE

    :param identifier:  local autorities id
    :return:
    """
    headers = {"x-api-version": "2", "accept": "application/json", "content-type": "application/json"}
    r = requests.get('http://api.ratings.food.gov.uk/Establishments?localAuthorityId={}'.format(identifier),
                     headers=headers)
    establishments = r.json()
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


def get_static_soton_data(town="Southampton"):
    """
    Gets static data from food standards website for southampton in xml format and converts it to dict
    :return: southampton hygiene data as dict
    """
    town_to_link_dict = get_hygiene_data_source()
    url = town_to_link_dict[town]
    print(url)
    r = requests.get(url)
    southampton_data = xmltodict.parse(r.text)['FHRSEstablishment']['EstablishmentCollection']["EstablishmentDetail"]
    return southampton_data


def update_hygiene_data_db(data):
    """
    adds hygiene data to specified mongodb database
    :param data: dict of documents to add
    """
    db = DbConnection().get_restaurant_db()
    for e in data:
        key = bson.son.SON({"FHRSID" : e["FHRSID"]})
        db.hygiene_data.update(key, e, upsert=True)


if __name__ == "__main__":
    data = get_static_soton_data()
    update_hygiene_data_db([bson.son.SON(establishment) for establishment in data])
