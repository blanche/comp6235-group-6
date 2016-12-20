import json
from collections import defaultdict, Counter
from scipy import stats
import matplotlib.pyplot as plt
import numpy

from db.connection import DbConnection

worst = {'Spelthorne',
         'Adur',
         'Selby',
         'Mid Ulster',
         'North Kesteven',
         'Wychavon',
         'Aylesbury Vale',
         'Rochdale',
         'South Northamptonshire',
         'Croydon'}

best = {'Fermanagh and Omagh',
        'Breckland',
        'Halton',
        'East Northamptonshire',
        'Allerdale',
        'Rossendale',
        'Corby',
        'Mid and East Antrim',
        'Stroud',
        'Isles of Scilly'}

union = set.union(worst, best)

bycouncil_both = defaultdict(list)
byconcil_price = defaultdict(list)
byconcil_cat = defaultdict(lambda: defaultdict(int))

for line in DbConnection().get_overall_collection().find({"hygiene.LocalAuthorityName": {"$in": list(union)}}):
    # for line in open("/home/lukas/dump/out.json"):
    # j = json.loads(line)
    j = line
    if 'hygiene' in j and 'LocalAuthorityName' in j['hygiene'] and j['hygiene']['RatingValue'] is not None:
        council = j['hygiene']['LocalAuthorityName']
        if council in union:
            if 'combined_rating' in j:
                bycouncil_both[council].append(
                    [j['combined_rating'], j['hygiene']['RatingValue']])
            if 'yelp' in j:
                if 'price' in j['yelp'] and j['yelp']['price'] is not None:
                    byconcil_price[council].append(j['yelp']['price'])
                if 'categories' in j['yelp']:
                    for cat in j['yelp']['categories']:
                        byconcil_cat[council][cat] += 1

f = open('drilldown.csv', 'w', 4096)
f.write(
    '"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"\n'.format("key", "ratings_avg", "ratings_std",
                                                                                "hygiene_avg", "hygiene_std",
                                                                                "r_value", "std_err", "len(val)",
                                                                                "avg_price", "stddev_price",
                                                                                "top_categories", "slope", "intercept"))
for key, val in bycouncil_both.items():
    val = [x for x in val if x is not None]
    x = [x[0] for x in val]
    y = [x[1] for x in val]
    ratings_std = numpy.std(x, axis=0)
    ratings_avg = sum(x) / float(len(x))
    hygiene_std = numpy.std(y, axis=0)
    hygiene_avg = sum(y) / float(len(y))

    council_prices = byconcil_price[key]
    avg_price = sum(council_prices) / float(len(council_prices))
    stddev_price = numpy.std(val, axis=0)

    top_categories = ",".join([x[0] for x in Counter(byconcil_cat[key]).most_common(5)])

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    # from https://stackoverflow.com/questions/7941226/add-line-based-on-slope-and-intercept-in-matplotlib
    abline_values = [slope * i + intercept for i in x]

    fig = plt.figure()
    plt.scatter(x, y)
    plt.title(key)
    plt.ylabel('hygiene')
    plt.xlabel('ratings')
    plt.plot(x, abline_values)
    plt.axis([0, 5.3, 0, 5.3])
    # plt.show()
    fig.savefig('pdf/' + key + ".pdf")

    fig = plt.figure()
    plt.hist(x)
    plt.xlabel('ratings')
    plt.title(key)
    fig.savefig('pdf/' + key + "_ratings_hist.pdf")

    fig = plt.figure()
    plt.hist(y)
    plt.xlabel('hygiene')
    plt.title(key)
    fig.savefig('pdf/' + key + "_hygiene_hist.pdf")

    f.write(
        '"{}",{},{},{},{},{},{},{},{},{},"{}",{},{}\n'.format(key, ratings_avg, ratings_std, hygiene_avg, hygiene_std,
                                                              r_value, std_err, len(val), avg_price, stddev_price,
                                                              top_categories, slope, intercept))
f.close()
