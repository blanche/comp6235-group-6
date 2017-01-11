from scipy import stats
import json
import numpy
from collections import defaultdict
import matplotlib.pyplot as plt

bycat = defaultdict(lambda: {"hygiene": [], "rating": []})

bycat_both = defaultdict(list)
bycouncil_both = defaultdict(list)
byprice_both = defaultdict(list)

bycat_price = defaultdict(list)
byconcil_price = defaultdict(list)

for line in open("/home/lukas/dump/out.json"):
    j = json.loads(line)
    if 'yelp' in j:
        if 'categories' in j['yelp']:
            for cat in j['yelp']['categories']:
                if 'hygiene' in j and 'RatingValue' in j['hygiene'] and j['hygiene']['RatingValue'] is not None:
                    bycat[cat]['hygiene'].append(j['hygiene']['RatingValue'])
                    if 'combined_rating' in j:
                        bycat_both[cat].append([j['combined_rating'], j['hygiene']['RatingValue']])
                        bycat[cat]['rating'].append(j['combined_rating'])

                if 'price' in j['yelp'] and j['yelp']['price'] is not None:
                    bycat_price[cat].append(j['yelp']['price'])

        if 'price' in j['yelp'] and j['yelp']['price'] is not None:
            # byprice[j['yelp']['price']]['rating'].append(j['yelp']['rating'])
            if 'hygiene' in j and 'LocalAuthorityName' in j['hygiene'] and j['hygiene']['RatingValue'] is not None:
                # byprice[j['yelp']['price']]['rating'].append(j['hygiene']['RatingValue'])
                byprice_both[j['yelp']['price']].append([j['yelp']['rating'], j['hygiene']['RatingValue']])

    if 'hygiene' in j and 'LocalAuthorityName' in j['hygiene'] and j['hygiene']['RatingValue'] is not None:
        if 'combined_rating' in j:
            bycouncil_both[j['hygiene']['LocalAuthorityName']].append(
                [j['combined_rating'], j['hygiene']['RatingValue']])
        if 'yelp' in j and 'price' in j['yelp'] and j['yelp']['price'] is not None:
            byconcil_price[j['hygiene']['LocalAuthorityName']].append(j['yelp']['price'])

f = open('bycat_all.csv', 'w', 4096)
f.write('"{}","{}","{}","{}","{}"\n'.format("key", "hygiene_avg", "len(hygiene)", "ratings_avg", "len(ratings)"))
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
        f.write('"{}",{},{},{},{}\n'.format(key, hygiene_avg, len(hygiene), ratings_avg, len(ratings)))
f.close()


def calcomat(list, filename, plot=False):
    f = open(filename, 'w', 4096)
    f.write(
        '"{}","{}","{}","{}","{}","{}","{}","{}"\n'.format("key", "ratings_avg", "ratings_std", "hygiene_avg",
                                                           "hygiene_std", "r_value", "std_err", "len(val)"))
    for key, val in list.items():
        val = [x for x in val if x is not None]
        if len(val) > 10:
            x = [x[0] for x in val]
            y = [x[1] for x in val]
            ratings_std = numpy.std(x, axis=0)
            ratings_avg = sum(x) / float(len(x))
            hygiene_std = numpy.std(y, axis=0)
            hygiene_avg = sum(y) / float(len(y))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            if plot:
                # from https://stackoverflow.com/questions/7941226/add-line-based-on-slope-and-intercept-in-matplotlib
                abline_values = [slope * i + intercept for i in x]
                plt.scatter(x, y)
                plt.plot(x, abline_values)
                plt.show()
            f.write(
                '"{}",{},{},{},{},{},{},{}\n'.format(key, ratings_avg, ratings_std, hygiene_avg, hygiene_std, r_value,
                                                     std_err, len(val)))
    f.close()


calcomat(bycouncil_both, 'bycouncil.csv')
calcomat(bycat_both, 'bycat.csv')
calcomat(byprice_both, 'byprice.csv')


def calc_by_price(list, filename):
    f = open(filename, 'w', 4096)
    f.write('"{}","{}","{}","{}"\n'.format("key", "avg", "std", "len(val)"))
    for key, val in list.items():
        if len(val) > 10:
            avg = sum(val) / float(len(val))
            std = numpy.std(val, axis=0)
            f.write('"{}",{},{},{}\n'.format(key, avg, std, len(val)))
    f.close()


calc_by_price(byconcil_price, 'price_bycouncil.csv')
calc_by_price(bycat_price, 'price_bycat.csv')
