from scipy import stats
import json
import numpy
from collections import defaultdict
import matplotlib.pyplot as plt

hygiene = []
rating = []

restaurant = []


for line in open("/home/lukas/dump/out.json"):
    j = json.loads(line)
    if 'combined_rating' in j:
        rating.append(j['combined_rating'])
        if 'hygiene' in j and 'RatingValue' in j['hygiene'] and j['hygiene']['RatingValue'] is not None:
            restaurant.append((j['combined_rating'], j['hygiene']['RatingValue']))
    if 'hygiene' in j and 'RatingValue' in j['hygiene'] and j['hygiene']['RatingValue'] is not None:
        hygiene.append(j['hygiene']['RatingValue'])

fig = plt.figure()
plt.hist(hygiene)
plt.xlabel('hygiene')
plt.title('Hygiene')
fig.savefig('hygiene_histogram.pdf')
fig = plt.figure()
plt.hist(rating)
plt.xlabel('rating')
plt.title('Ratings')
fig.savefig('rating_histogram.pdf')

x = [x[0] for x in restaurant]
y = [x[1] for x in restaurant]

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
# from https://stackoverflow.com/questions/7941226/add-line-based-on-slope-and-intercept-in-matplotlib
abline_values = [slope * i + intercept for i in x]

print(r_value)


fig = plt.figure()
plt.scatter(x, y)
plt.title("Correlation between hygiene and ratings")
plt.ylabel('hygiene')
plt.xlabel('ratings')
plt.plot(x, abline_values)
plt.axis([0, 5.3, 0, 5.3])
fig.savefig("correlation.pdf")

