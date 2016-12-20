from scipy import stats
import json
import numpy
from collections import defaultdict
import matplotlib.pyplot as plt

byprice_hygiene = defaultdict(list)
byprice_rating = defaultdict(list)

for line in open("/home/lukas/dump/out.json"):
    j = json.loads(line)
    if 'yelp' in j:
        if 'price' in j['yelp'] and j['yelp']['price'] is not None:
            if 'review_count' in j['yelp'] and j['yelp']['review_count'] > 10:
                if 'hygiene' in j and 'RatingValue' in j['hygiene'] and j['hygiene']['RatingValue'] is not None:
                    byprice_hygiene[j['yelp']['price']].append(j['hygiene']['RatingValue'])
                if 'combined_rating' in j:
                    byprice_rating[j['yelp']['price']].append(j['combined_rating'])


def calc(dictlist):
    x = []
    y = []
    for price, list_of_values in dictlist.items():
        for value in list_of_values:
            x.append(price)
            y.append(value)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    print("{},{},{}".format(slope, intercept, r_value))
    print("###")
    for key in dictlist:
        val = dictlist[key]
        print("{},{}".format(key, sum(val) / len(val)))

    print("##########")

calc(byprice_rating)
calc(byprice_hygiene)
