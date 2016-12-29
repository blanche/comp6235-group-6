from scipy import stats
import json
import numpy
from collections import defaultdict
import matplotlib.pyplot as plt

bycat = defaultdict(lambda: {"hygiene": [], "rating": []})
bycat_both = defaultdict(list)
bycat_price = defaultdict(list)
bycouncil_both = defaultdict(list)
byconcil_price = defaultdict(list)
byprice = defaultdict(lambda: {"hygiene": [], "rating": []})
byprice_both = defaultdict(list)

for line in open("/home/lukas/out.json"):
    j = json.loads(line)
    if 'yelp' in j:
        if 'categories' in j['yelp']:
            for cat in j['yelp']['categories']:
                bycat[cat]['rating'].append(j['yelp']['rating'])
                if 'hygiene' in j and 'RatingValue' in j['hygiene'] and j['hygiene']['RatingValue'] is not None:
                    bycat[cat]['hygiene'].append(j['hygiene']['RatingValue'])
                    bycat_both[cat].append([j['yelp']['rating'], j['hygiene']['RatingValue']])

                if 'price' in j['yelp'] and j['yelp']['price'] is not None:
                    bycat_price[cat].append(j['yelp']['price'] )

        if 'hygiene' in j and 'LocalAuthorityName' in j['hygiene'] and j['hygiene']['RatingValue'] is not None:
            bycouncil_both[j['hygiene']['LocalAuthorityName']].append(
                [j['yelp']['rating'], j['hygiene']['RatingValue']])
            if 'price' in j['yelp'] and j['yelp']['price'] is not None:
                byconcil_price[j['hygiene']['LocalAuthorityName']].append(j['yelp']['price'])
        if 'price' in j['yelp'] and j['yelp']['price'] is not None:
            byprice[j['yelp']['price']]['rating'].append(j['yelp']['rating'])
            if 'hygiene' in j and 'LocalAuthorityName' in j['hygiene'] and j['hygiene']['RatingValue'] is not None:
                byprice[j['yelp']['price']]['rating'].append(j['hygiene']['RatingValue'])
                byprice_both[j['yelp']['price']].append([j['yelp']['rating'], j['hygiene']['RatingValue']])



for key, val in bycat.items():
    hygiene_avg = ""
    ratings_avg = ""

    hygiene = val['hygiene']
    hygiene = [x for x in hygiene if x is not None]
    if len(hygiene) > 10:
        hygiene_avg = sum(hygiene) / float(len(hygiene))
    ratings = val['rating']
    ratings = [x for x in ratings if x is not None]
    if len(ratings) > 10:
        ratings_avg = sum(ratings) / float(len(ratings))
    if hygiene_avg != "" or ratings_avg != "":
        print("{}\t{}\t{}\t{}\t{}".format(key, hygiene_avg, len(hygiene), ratings_avg, len(ratings)))

def calcomat(key, val):
    val = [x for x in val if x is not None]
    if len(val) > 10:
        x = [x[0] for x in val]
        y = [x[1] for x in val]
        ratings_std = numpy.std(x, axis=0)
        ratings_avg = sum(x) / float(len(x))
        hygiene_std = numpy.std(y, axis=0)
        hygiene_avg = sum(y) / float(len(y))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        # from https://stackoverflow.com/questions/7941226/add-line-based-on-slope-and-intercept-in-matplotlib
        # abline_values = [slope * i + intercept for i in x]
        # plt.scatter(x, y)
        # plt.plot(x, abline_values)
        # plt.show()
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(key, ratings_avg, ratings_std, hygiene_avg, hygiene_std, r_value,
                                                      std_err, len(val)))


for k, v in bycouncil_both.items():
    calcomat(k, v)

for k, v in bycat_both.items():
    calcomat(k, v)

for k, v in byprice_both.items():
    calcomat(k, v)

for key, val in byconcil_price.items():
    if len(val) > 10:
        avg = sum(val) / float(len(val))
        std = numpy.std(val, axis=0)
        print("{}\t{}\t{}\t{}".format(key, avg, std, len(val)))


for key, val in bycat_price.items():
    if len(val) > 10:
        avg = sum(val) / float(len(val))
        std = numpy.std(val, axis=0)
        print("{}\t{}\t{}\t{}".format(key, avg, std, len(val)))
