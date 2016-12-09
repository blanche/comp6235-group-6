import pandas as pd
from src.db.connection import DbConnection
import csv
import os

def _connect_mongo():

  conn = DbConnection()
  return conn


def read_mongo_overall():
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    overall_conn = _connect_mongo().get_overall_collection()
    cursor = overall_conn.find({})
    return cursor


def put_into_df(data, id="FHRSID"):
    #List of records
    df =  pd.DataFrame(list(data))

    # Delete the _id
    if id != "_id":
        del df['_id']

    return df


def get_relvent_fields_from_overall():
    all_data = [c for c in read_mongo_overall()]
    all_records = []
    for r in all_data:
        analyse_dict = {}
        if "hygiene" in r:
            analyse_dict["FHRSID"] = r["FHRSID"]
            if "google" in r:
                analyse_dict["google_rating"] = r["google"]["rating"]
                if "types" in r["google"]:
                    analyse_dict["types"] = r["google"]["types"]
            if "yelp" in r:
                analyse_dict["yelp_rating"] = r["yelp"]["rating"]
                analyse_dict["yelp_pricing"] = r["yelp"]["rating"]
            analyse_dict["hygiene_rating"] = r["hygiene"]["RatingValue"]
            if "Scores" in r["hygiene"] and r["hygiene"]["Scores"] is not None:
                if "ConfidenceInManagement" in r["hygiene"]["Scores"]:
                    analyse_dict["hygiene_scores_management"] = r["hygiene"]["Scores"]["ConfidenceInManagement"]
                    analyse_dict["hygiene_scores_structural"] = r["hygiene"]["Scores"]["Structural"]
                    analyse_dict["hygiene_scores_hygiene"] = r["hygiene"]["Scores"]["Hygiene"]

            if "PostCode" in r["hygiene"]:
                analyse_dict["postcode"] = r["hygiene"]["PostCode"]
            analyse_dict["authority_name"] = r["hygiene"]["LocalAuthorityName"]
            analyse_dict["name"] = r["hygiene"]["BusinessName"]
            all_records.append(analyse_dict)
    return all_records

def write_to_csv(data_list):
    df = pd.DataFrame(data_list)
    df.to_csv('data.csv')



if __name__ == "__main__":
    data = get_relvent_fields_from_overall()
    write_to_csv(data)