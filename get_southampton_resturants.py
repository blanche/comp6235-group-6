
import requests
import bson
import xmltodict
from db.connection import DbConnection

def get_southampton_resturants_by_authorities_id(id):
    """
    gets all resturants the has authorites id {id}. NOT WORKING AS API IS BROKE

    :param id:  local autorities id
    :return:
    """
    headers = {"x-api-version": "2", "accept": "application/json", "content-type":"application/json"}
    r = requests.get('http://api.ratings.food.gov.uk/Establishments?localAuthorityId={}'.format(id),headers=headers)
    establishments = r.json()
    return r.json()

def get_authority_id(name):
    """
    pass in name of authority i.e southampton and returns the id

    :param name: City/Town
    :return: Id
    """

    headers = {"x-api-version": "2", "accept": "application/json", "content-type":"application/json"}
    r = requests.get('http://api.ratings.food.gov.uk/Authorities/basic', headers=headers)
    authorities = r.json()["authorities"]
    southampton_id = [x["LocalAuthorityId"] for x in authorities if x["Name"] == name.capitalize()]
    return southampton_id[0]

def get_static_soton_data():
    """
    Gets static data from food standards website for southampton in xml format and converts it to dict
    :return: southampton hygine data as dict
    """

    r = requests.get('http://ratings.food.gov.uk/OpenDataFiles/FHRS877en-GB.xml')
    southampton_data = xmltodict.parse(r.text)['FHRSEstablishment']['EstablishmentCollection']["EstablishmentDetail"]
    return southampton_data


def update_hygine_data_db(data):
    """
    adds hygine data to specified mongodb database
    :param data: dict of documents to add
    """
    db = DbConnection().get_resturant_db()
    for e in data:
        key = bson.son.SON({"FHRSID" : e["FHRSID"]})
        db.hygine_data.update(key, e, upsert=True)

if __name__ == "__main__":
    data = get_static_soton_data()
    update_hygine_data_db([bson.son.SON(establishment) for establishment in data])
