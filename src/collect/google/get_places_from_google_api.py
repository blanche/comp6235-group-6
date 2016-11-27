import time
from difflib import SequenceMatcher

import bson
import requests

from db.connection import DbConnection

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
    # """
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


# OrderedDict([('FHRSID', '219985'), ('LocalAuthorityBusinessID', '00080/0113/2/000'), ('BusinessName', "Yates's"), ('BusinessType', 'Pub/bar/nightclub'), ('BusinessTypeID', '7843'), ('AddressLine1', '113 - 117 Above Bar Street'), ('AddressLine2', 'Southampton'), ('PostCode', 'SO14 7FH'), ('RatingValue', '4'), ('RatingKey', 'fhrs_4_en-GB'), ('RatingDate', '2015-02-17'), ('LocalAuthorityCode', '877'), ('LocalAuthorityName', 'Southampton'), ('LocalAuthorityWebSite', 'http://www.southampton.gov.uk'), ('LocalAuthorityEmailAddress', 'hygiene.rating@southampton.gov.uk'), ('Scores', OrderedDict([('Hygiene', '5'), ('Structural', '5'), ('ConfidenceInManagement', '10')])), ('SchemeType', 'FHRS'), ('NewRatingPending', 'False'), ('Geocode', OrderedDict([('Longitude', '-1.40485800000000'), ('Latitude', '50.90653100000000')]))])
# {'results': [{'scope': 'GOOGLE', 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png', 'reference': 'CmRSAAAAmK_NFpDUiIOC16sTErn06GvJ3E7wT17tW8CZktKZfjuYhc5B31eNmWla6u7lA7xfkXyLrRf2nbuL7M474KMeY-cXU4WCXwZF7aE0KF4UpOSEVGKOw9rD9XhqM3BuaN4XEhBTMWkOxpw61kzki9d9Sci2GhSZi9_Vc-IsYc3_9XE5sqiaJASP8Q', 'photos': [{'height': 5312, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/107128340975962597462/photos">Scott Jacobs</a>'], 'width': 2988, 'photo_reference': 'CoQBdwAAANaE5ys1OzwkSWytB7l2umCX07M8b3ujxlB53cmX0ArO4CITtrpQllpxVoEW5T15VKwSYuCAGI4DNQNXv_RrLt4FFuezqxxtLAf-P7E8YHSqgGfUANFEHi1eonK0FuG-0ieUoOzvev0qpyy4rtr4ULWRYO6NBoZtDRjIUHQ2wranEhB3ThsUetQXm4i-nasiBnQTGhQGuHgJRfALTGE2FLmb2U-xY7Lsnw'}], 'opening_hours': {'weekday_text': [], 'open_now': True}, 'name': 'Bella Italia Southampton Above Bar', 'place_id': 'ChIJbzwqarF2dEgRphZ43xb2YaU', 'rating': 3.7, 'id': '5323b05761a20b3d45d719d770e128ca413dcd73', 'price_level': 2, 'geometry': {'location': {'lng': -1.404649, 'lat': 50.906319}, 'viewport': {'southwest': {'lng': -1.40471945, 'lat': 50.90631669999998}, 'northeast': {'lng': -1.40443765, 'lat': 50.90632590000001}}}, 'vicinity': '107 Above Bar Street, Southampton', 'types': ['restaurant', 'food', 'point_of_interest', 'establishment']}], 'html_attributions': [], 'status': 'OK'}
# {'html_attributions': [], 'results': [], 'status': 'ZERO_RESULTS'}
#{'status': 'OK', 'html_attributions': [], 'result': {'scope': 'GOOGLE', 'id': 'd32e898f68f373615c55d1f785cd291932ac6d6f', 'url': 'https://maps.google.com/?cid=11893248350314747505', 'types': ['night_club', 'bar', 'point_of_interest', 'establishment'], 'opening_hours': {'open_now': True, 'periods': [{'close': {'day': 1, 'time': '0030'}, 'open': {'day': 0, 'time': '1000'}}, {'close': {'day': 2, 'time': '0000'}, 'open': {'day': 1, 'time': '0900'}}, {'close': {'day': 3, 'time': '0000'}, 'open': {'day': 2, 'time': '0900'}}, {'close': {'day': 4, 'time': '0000'}, 'open': {'day': 3, 'time': '0900'}}, {'close': {'day': 5, 'time': '0130'}, 'open': {'day': 4, 'time': '0900'}}, {'close': {'day': 6, 'time': '0130'}, 'open': {'day': 5, 'time': '0900'}}, {'close': {'day': 0, 'time': '0130'}, 'open': {'day': 6, 'time': '0900'}}], 'weekday_text': ['Monday: 9:00 AM – 12:00 AM', 'Tuesday: 9:00 AM – 12:00 AM', 'Wednesday: 9:00 AM – 12:00 AM', 'Thursday: 9:00 AM – 1:30 AM', 'Friday: 9:00 AM – 1:30 AM', 'Saturday: 9:00 AM – 1:30 AM', 'Sunday: 10:00 AM – 12:30 AM']}, 'rating': 3.6, 'address_components': [{'short_name': '113-117', 'types': ['street_number'], 'long_name': '113-117'}, {'short_name': 'Above Bar St', 'types': ['route'], 'long_name': 'Above Bar Street'}, {'short_name': 'Southampton', 'types': ['locality', 'political'], 'long_name': 'Southampton'}, {'short_name': 'Southampton', 'types': ['postal_town'], 'long_name': 'Southampton'}, {'short_name': 'Southampton', 'types': ['administrative_area_level_2', 'political'], 'long_name': 'Southampton'}, {'short_name': 'England', 'types': ['administrative_area_level_1', 'political'], 'long_name': 'England'}, {'short_name': 'GB', 'types': ['country', 'political'], 'long_name': 'United Kingdom'}, {'short_name': 'SO14 7FH', 'types': ['postal_code'], 'long_name': 'SO14 7FH'}], 'geometry': {'location': {'lat': 50.9065386, 'lng': -1.4046639}, 'viewport': {'southwest': {'lat': 50.9065341, 'lng': -1.40473355}, 'northeast': {'lat': 50.9065521, 'lng': -1.40445495}}}, 'reference': 'CmRSAAAAn4J6eDN11eymjA5IyIPbzlHseepAs-gDLhEkHJjBUDZfWObmJwazN0fdORFN9ujqss9XHjlDhZ-f4SRgCPx1NDVNkJdlwyexhSmHfkl4z2srFpSGhK2v56fYmUprx4GCEhDWyAgWT16ZPRhVDjguAJttGhTy42odFZKFNOEG2Go3QA-D4Ohraw', 'website': 'http://www.weareyates.co.uk/southampton', 'vicinity': '113-117 Above Bar Street, Southampton', 'adr_address': '<span class="street-address">113-117 Above Bar St</span>, <span class="locality">Southampton</span> <span class="postal-code">SO14 7FH</span>, <span class="country-name">UK</span>', 'name': "Yates's", 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/bar-71.png', 'formatted_address': '113-117 Above Bar St, Southampton SO14 7FH, UK', 'international_phone_number': '+44 23 8063 4609', 'place_id': 'ChIJnSOHbLF2dEgRcdYCilxODaU', 'photos': [{'height': 1836, 'photo_reference': 'CoQBdwAAAA9QgzNn22XtSqCmsBuyUbx7PVdf7_Fzm56iqaEaCv2jOTqB6F2aClVplfuz5NVACUrO0xU5lUeC8Dp6nKvulGfkdHU0rrlSlDtao7cF4fnOjgeZFPkuFmWMLbzMULLYOSxeb4C5Zh8z9DOcSg3f0EOneHyfFyvfLDjDO3CwIaFyEhCJLQJMKwi4658LHA94zpvuGhQTM60Aw4RZ_jwSrDqFkiHan8ohTQ', 'width': 3264, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/104406031029400096501/photos">Dean Sarnecki</a>']}, {'height': 3120, 'photo_reference': 'CoQBdwAAAENO5GN4RUAgqSNP-CvkU0Pora5-19zjdj4VPxN5svduFRjM8ukCOYvMPXecGtBW9ozDaSPfhaULsRJccwruLRjQJKalWeCv-qmQ-XPnbpPV2igO13kkpcfT6gZBOSiz7sntYmIToKg6bprWxGhsQBF8Gf0kXP7pc_HLX8TP_LUeEhA502ebzzM4z9P4YiRn3H_cGhT5rMDntEsdSp3XeRrg2MPYkIayKA', 'width': 4160, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/115573265010777455910/photos">Sergio Reche</a>']}, {'height': 3120, 'photo_reference': 'CoQBdwAAAGi7BqQ_7n_uSMJGJxFT9X4KNna46oi858_aaewYcUSBeFwhvFHcUra_n3A7WmuLVytDRlLS1q92sEEYI1fKWAtTNbGDHAURvlTAKRRpD7QHPjk5Cku3g9qU6pawOYqW8F6KoO01sR9PHytwubR2VKx5xgDaUxlq-nxzxn_uN6UBEhDjozSSGPAFN8KRWgWyKky3GhR-vnvmkY_YNWXl_0VXyYcEt8n_cw', 'width': 4160, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/107962197957124893026/photos">Rafał Burda</a>']}, {'height': 2322, 'photo_reference': 'CoQBdwAAAHE4kSRBdLTsU8sZ0QLSVrIm90Vj-UerxlXI_pePThvXPOrwlNUXtNsDP79u06A3cgJY1U5LofKarA8CQWpWmxZgEMBGuLCf0nu-jeJ8yFCB3U6t9IuNqvXbLrGcdcnqzbfNb39BU309vVmE-QqcOKt5nj2xhafWyXQCnjwg8MLuEhBSTuwjlVJPqu7inIhbWCWgGhQN0FDYw3PyGDikpQA4rR_bpSKbIQ', 'width': 4128, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/112138092058895230487/photos">Victor Meirinhos</a>']}, {'height': 1836, 'photo_reference': 'CoQBdwAAAOH2g1AEfYbsNmKdRhAy5IOk24X0K-zG7sWTOmDLLWw_-k4gT8vnnBn2zpzMr9b8Hdpikiwlk9KNAA3qjbgO_Ur7g-uI1dXEVPtyQ-85qvZfyxXKH5NxjdkPFntmKCo-VXSXXn_UalECh5DeBksnvFkxQiLwnqs3Pck6m_Y7jc2jEhD3w5JC0MGh7CLYf4Evbd5nGhTx537siCkTJd3zJcAH9l2Har2JpA', 'width': 3264, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/114848289857087347228/photos">Daz Davies</a>']}, {'height': 4160, 'photo_reference': 'CoQBdwAAADD3qsLgUqeE5XHBA89fprh8dZlOvETe4epxnxhmxkVqnlz0Lt9x_Afdy6jw4HB5yBL33isJkkjV-rCTv0hHtPKB2V_08h5NmYjQx4aOW8H-iKTvyd9MRHLGu5t1ETooyuz9pX3i0d9FSgsA9oK9MMB39ZUvk3HBPVkDNE0Xrwy_EhC_zJkmenxz6PzB9HTh3w8tGhToYcjzxu6AmIZiz-kDwI1nmwJiEw', 'width': 3120, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109460487939403832973/photos">Annalisa De Lorenzis</a>']}, {'height': 3024, 'photo_reference': 'CoQBdwAAAMs6NFAT5u0k2AJYAfdSbq759vvB-BRyF17amhYt-Qws8GxFqhDGODXOimQt0B4ZFvVwUf3qZj8uFwAamPFJyflsAJunuYG2I98Rn0VGpQDg8W-5pfKRIL93FQ5iFRKz7nXRFrQOzd8t0Ydd1Qx_25BBxXRxeaDUOUljd4a0-lrhEhCpNp8GIES74jvPyuPeYjJlGhSlB_adjoTfSgMUfgtI_uXrVGcUGA', 'width': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/114888530632638710993/photos">Yuya Tanizaki</a>']}, {'height': 4160, 'photo_reference': 'CoQBdwAAAJIuTU5rlD2aLoUmE-ayVTr0MPrn-eDB1Pg0xQsQw4gND4aHbljCXtxCMmlXP6Yc_r0Gp3VYoQ8f9W1KTObyE8xEWtjvIqtOI6rzrPKQQHhGWTY0j5V3QJ1fr4RxiFTuqH4zk3O7OmqrwQBX_rVQiZn4gfovGNFCh3r0kTGeOyR-EhDAi-i165ErkL6POZGQznaeGhQkrOh7zMsy5wvtiX61W0T_XSQK_g', 'width': 2336, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/100607394662409581765/photos">Iana Florentina</a>']}, {'height': 2560, 'photo_reference': 'CoQBdwAAAPNVFhIHumhx7xq12i41owYYOojAkRshmNEhsyvrzIBVHv6HXfYAxlBNOUkYxXCUaggAU_0qUkoWopGELPN4pAbymsppyxq0pGnReMXbRwAYyRz0LBDmfofNbbSoCj0bG43wpIVO4GruPEd9UlGh1UkGAfoB2qDM539aALNG3SnHEhC2dm8pHrnh5vXS_5rQs0IgGhRiVLSxXdXJa8EQQ4xKME0Pj1ADVw', 'width': 1536, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/106252999932382191167/photos">John Berntsen</a>']}, {'height': 2988, 'photo_reference': 'CoQBdwAAAC9nEAfaKipNiOa4LGKkRPLsZpl97qv1aO5EYmOGnf-Az0NB45HXY_iA-ETbRN34v4SLtUrB1KNZmAmx5bn0V452MBH1L2CNlcm8djyTgHs_iMqyDDQd8uJ7HMNb9hdtHeQVr65JkGP0qHCvU5FIUGa1x13NPuOw6fxq_sxODyA5EhBrmf3_H0v14rcaQgSMcjwFGhQQUL9ucau8bn3BbWiZW3AKppMS7w', 'width': 5312, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/106418606086672443065/photos">Kelly Crews</a>']}], 'utc_offset': 0, 'formatted_phone_number': '023 8063 4609', 'reviews': [{'text': "Similar to spoons, very cheap and cheerful. Upstairs is very well decorated and is popular with people of all ages. I'd say stay away when there's a game on; it gets very loud as there are TVs everywhere (great if you're a sports fan)", 'rating': 4, 'author_name': 'Connie', 'language': 'en', 'author_url': 'https://plus.google.com/100255436754185872702', 'time': 1477336624, 'aspects': [{'type': 'overall', 'rating': 2}]}, {'text': 'Lovely bar up front but the staff need to learn how to clean the rest of the place, food under the table and on top. Food was ok, but could do with having a little more on the plate as I walked out still hungry.', 'rating': 2, 'author_name': 'Adam Glover', 'language': 'en', 'author_url': 'https://plus.google.com/113162763438524488581', 'time': 1475935419, 'aspects': [{'type': 'overall', 'rating': 0}]}, {'time': 1468854565, 'text': "Male member of staff was very polite, forthcoming and attentive. For that alone I'll put this pub in Southampton as a 1st in my list to go for a drink. ", 'rating': 5, 'author_name': 'Pāvels Vasiļenko', 'language': 'en', 'author_url': 'https://plus.google.com/106041925290406744107', 'profile_photo_url': '//lh3.googleusercontent.com/-GBGWcBBMU0k/AAAAAAAAAAI/AAAAAAACiQg/V4V4ksibkUk/photo.jpg', 'aspects': [{'type': 'overall', 'rating': 3}]}, {'time': 1476210018, 'text': 'Drinks are good, but pricey. Nice atmosphere.', 'rating': 4, 'author_name': 'Jack Isaacs', 'language': 'en', 'author_url': 'https://plus.google.com/101128141001054323444', 'profile_photo_url': '//lh6.googleusercontent.com/-n3PViJDVb7o/AAAAAAAAAAI/AAAAAAAATlU/jb6OxioMc38/photo.jpg', 'aspects': [{'type': 'overall', 'rating': 2}]}, {'time': 1449220098, 'text': "Popped in there yesterday. It has recently been refurbished and is warm an pleasant but there were 3 members of staff who were in the kitchen when I arrived and therefore I had to wait 5 minutes before they surfaced and I could be served. The tables were grubby and still had glasses, sauces and bits of food in them. One of the staff removed the dirty plates but there was no evidence of a cloth or cleaning solution and he didn't return to collect the glasses or sauces. Not impressed. It appears to me that the management need to spend time training the staff on customer service and hygiene.", 'rating': 1, 'author_name': 'Caroline Belas', 'language': 'en', 'author_url': 'https://plus.google.com/117008942481474236090', 'profile_photo_url': '//lh6.googleusercontent.com/-zwNblUJjtDM/AAAAAAAAAAI/AAAAAAAACSs/LXiUzxqvUCg/photo.jpg', 'aspects': [{'type': 'overall', 'rating': 0}]}]}}

