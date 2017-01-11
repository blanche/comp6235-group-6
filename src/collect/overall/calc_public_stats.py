from scipy import stats
import json
import numpy
from collections import defaultdict
import matplotlib.pyplot as plt

# std_devs = []
# for line in open("/home/lukas/dump/out.json"):
#     j = json.loads(line)
#
#     ratings = []
#     if 'yelp' in j and 'rating' in j['yelp']:
#         ratings.append(j['yelp']['rating'])
#     if 'google' in j and 'rating' in j['google'] and j['google']['rating'] != 'NONE':
#         ratings.append(j['google']['rating'])
#     if 'justEat' in j and 'avgRating' in j['justEat']:
#         ratings.append(j['justEat']['avgRating'])
#
#     if len(ratings) > 2:
#         std_dev = numpy.std(ratings)
#         std_devs.append(std_dev)
#
# print(sum(std_devs) / len(std_devs))

yg = []
yj = []
jg = []
for line in open("/home/lukas/dump/out.json"):
    j = json.loads(line)
    if 'yelp' in j and 'rating' in j['yelp']:
        if 'google' in j and 'rating' in j['google'] and j['google']['rating'] != 'NONE':
            ratings = [j['yelp']['rating'], j['google']['rating']]
            yg.append(ratings)
        if 'justEat' in j and 'avgRating' in j['justEat']:
            ratings = [j['yelp']['rating'], j['justEat']['avgRating']]
            yj.append(ratings)
    if 'justEat' in j and 'avgRating' in j['justEat']:
        if 'google' in j and 'rating' in j['google'] and j['google']['rating'] != 'NONE':
            ratings = [j['justEat']['avgRating'], j['google']['rating']]
            jg.append(ratings)


def calcomat(ratings):
    x = [x[0] for x in ratings]
    y = [x[1] for x in ratings]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print("{}".format(r_value))
    # from https://stackoverflow.com/questions/7941226/add-line-based-on-slope-and-intercept-in-matplotlib
    abline_values = [slope * i + intercept for i in x]
    plt.scatter(x, y)
    plt.plot(x, abline_values)
    plt.show()


calcomat(yg)
calcomat(yj)
calcomat(jg)
