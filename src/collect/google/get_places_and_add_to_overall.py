from collect.google.get_places_from_google_api import get_google_places_for_current_of_higene_data_establishments

from collect.google.combine_to_overall import combine_google_found_to_overall


def get_and_combine_to_overall():
    get_google_places_for_current_of_higene_data_establishments()
    combine_google_found_to_overall()