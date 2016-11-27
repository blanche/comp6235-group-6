import bson

from db.connection import DbConnection


# var docs = db.hygiene_data.find({})
# docs.forEach(function(doc){db.overall.insert(doc)});


def combine_google_found_to_overall():
    db = DbConnection().get_restaurant_db()
    google_data = db.google_reviews_found.find({})

    for e in google_data:
        add_to_overall = {
            "place_id": e["place_id"],
            "url": e["url"],
            "types": e["types"],
            "icon" : e["icon"],
            "geometry" : e["geometry"],
        }

        if "reviews" in e.keys():
            add_to_overall["reviews"] = e["reviews"]
        else:
            add_to_overall["reviews"] = []


        if "rating" in e.keys():
            add_to_overall["rating"] = e["rating"]
        else:
            add_to_overall["rating"] = "NONE"

        if "permanently_closed" in e.keys():
            add_to_overall["permanently_closed"] = e["permanently_closed"]
        else:
            add_to_overall["permanently_closed"] = False

        key = bson.son.SON({"FHRSID": e["FHRSID"]})
        data = bson.son.SON({"google":add_to_overall})
        print(e["FHRSID"])
        db.overall.find_and_modify(query=key, update={"$set": data}, upsert=False,
                                     full_response=True)

    print(google_data.count())


if __name__ == "__main__":
    combine_google_found_to_overall()


    #Google
    #rating
    #reviews
    #place_id
    #website
    #types


    #Hygiene Data
    #FHRSID
    #Buisness Name
    #Postcode
    #