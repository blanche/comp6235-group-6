from flask import Flask, request
from flask_restful import Resource, Api
from src.db.connection import DbConnection
from bson import json_util
from itertools import groupby, tee
import json
from collections import OrderedDict
from collections import Counter

app = Flask(__name__)
api = Api(app)
db = DbConnection().get_restaurant_db()

class OverviewListAPI(Resource):
    def get(self):
        query = {k: v for (k, v) in request.args.items()}
        print("Request made")
        #replace white space
        for k,v in query.items():
            k = k.replace("%20", " ")
            query[k] = v.replace("%20", " ")

        for k,v in query.items():
            if "__" in v:
                try:
                    search_value = float(v.split("__")[1])
                except ValueError:
                    search_value = v.split("__")[1]

                query[k] = {v.split("__")[0]:search_value}
        cursor = db.overall.find(query)
        json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
        print("return results {}".format(len(json_docs)))
        return json_docs


class OverViewAPI(Resource):
    def get(self, id):
        db.overall.find({"FHRSID":id})

class CouncilNameListAPI(Resource):
    def get(self):
        query = {}
        cursor = db.hygiene_data.distinct("LocalAuthorityName")
        json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
        return json_docs

class CouncilStatsAPI(Resource):
    def get(self, council_name):
        query = {"LocalAuthorityName":council_name}
        cursor = db.localAuthStats.find(query)
        json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
        return json_docs

class CouncilWordReviewAPI(Resource):
    def get(self, council_name):
        query = {"LocalAuthorityName": council_name}
        cursor = db.localAuthReviews.find(query)
        json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
        return  json_docs
		
class CoulcilCategoryLowerAvgAPI(Resource):
    def get(self, council_name):
        query = {"LocalAuthorityName": council_name}
        cursor = db.AuthLowerThanAvg.find(query)
        json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
        return  json_docs

class PdfCalculationAPI(Resource):

    def get(self, council_name):
        google, yelp, hygiene = [],[],[]
        query = {"hygiene.LocalAuthorityName":council_name}
        returnValues = {"hygiene.RatingValue":1, "google.rating":1, "yelp.rating":1}
        cursor = db.overall.find(query, returnValues)
        for doc in cursor:
            if "google" in doc:
                rating = doc["google"]["rating"]
                if rating != "NONE": google.append(rating)
            if "yelp" in doc:
                yelp.append(doc["yelp"]["rating"])
            if "hygiene" in doc:
                hygiene.append(doc["hygiene"]["RatingValue"])

        google_count = dict(Counter(google))
        yelp_count = dict(Counter(yelp))
        hygiene_count = dict(Counter(hygiene))
        json_dumps = json.dumps({"google":google_count, "yelp":yelp_count, "hygiene":hygiene_count}, default=json_util.default)
        return json_dumps
		
class CouncilCategorystatsAPI(Resource):

    def get(self, council_name):
        query = {"LocalAuthorityName":council_name}
        cursor = db.localAuthCategory.find(query)
        json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
        return json_docs

class CategoriesTopFiveBottomFiveAPI(Resource):
    def get(self, category):
        MIN_NUMBER_OF_RESTURANTS_NEEDED = 5
        query = {"yelp.categories":category}
        fields_to_find = ["google.rating","yelp.rating","hygiene.RatingValue","hygiene.LocalAuthorityName"]
        cursor = db.overall.find(query,fields_to_find)
        records = [doc for doc in cursor]

        google_top_bottom_5 = {"top":[], "bottom":[]}
        yelp_top_bottom_5 = {"top": [], "bottom": []}
        hygiene_top_bottom_5 = {"top": [], "bottom": []}

        overall_data = OrderedDict()

        data = sorted(records, key=lambda x:x["hygiene"]["LocalAuthorityName"])
        for key, group in groupby(data, lambda x:x["hygiene"]["LocalAuthorityName"]):
            g1, g2, g3 ,g4 = tee(group,4)
            count_g = sum(1 for _ in g1)
            if count_g>=MIN_NUMBER_OF_RESTURANTS_NEEDED:
                google_average = sum([rec["google"]["rating"]
                                        if "google" in rec and type(rec["google"]["rating"]) != type("str") and rec["google"]["rating"] != None
                                         else 0
                                         for rec in g2])/count_g

                yelp_average = sum([rec["yelp"]["rating"] if "yelp" in rec else 0 for rec in g3])/count_g

                hygiene_average = sum([rec["hygiene"]["RatingValue"]
                                        if "hygiene" in rec and rec["hygiene"]["RatingValue"] != None
                                        else 0
                                        for rec in g4])/count_g

                overall_data[key] = {"google":google_average, "yelp":yelp_average, "hygiene":hygiene_average}
            else:
                overall_data[key] = {"google":0, "yelp":0, "hygiene":0}

        yelp_data = {k: v for k, v in overall_data.items() if v["yelp"] != 0}
        yelp_top_bottom_5["top"] =  sorted(yelp_data.items(), key=lambda x : x[1]["yelp"], reverse=True)[:5]
        yelp_top_bottom_5["bottom"] = sorted(yelp_data.items(), key=lambda x : x[1]["yelp"], reverse=False)[:5]
		
        #filter 0's from hygiene
        hygiene_data = {k: v for k, v in overall_data.items() if v["hygiene"] != 0}
        hygiene_top_bottom_5["top"] =  sorted(hygiene_data.items(), key=lambda x : x[1]["hygiene"], reverse=True)[:5]
        hygiene_top_bottom_5["bottom"] = sorted(hygiene_data.items(), key=lambda x : x[1]["hygiene"], reverse=False)[:5]

        #filter 0's from google
        google_data = {k: v for k, v in overall_data.items() if v["google"] != 0}
        google_top_bottom_5["top"] = sorted(google_data.items(), key=lambda x: x[1]["google"], reverse=True)[:5]
        google_top_bottom_5["bottom"] = sorted(google_data.items(), key=lambda x: x[1]["google"], reverse=False)[:5]
        json_dumps = json.dumps({"yelp":yelp_top_bottom_5, "hygiene":hygiene_top_bottom_5, "google":google_top_bottom_5},
                                default=json_util.default)
        return json_dumps
		
class CategoryStatsAPI(Resource):
    def get(self):
        query = {}
        cursor = db.CategoryStats.find(query)
        json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
        return json_docs
		
api.add_resource(CategoryStatsAPI, '/api/v1/categorystats/')
api.add_resource(CoulcilCategoryLowerAvgAPI, '/api/v1/councillowerthanavg/<string:council_name>')
api.add_resource(CouncilCategorystatsAPI, '/api/v1/councilcategorystats/<string:council_name>')
api.add_resource(PdfCalculationAPI, '/api/v1/councilPdf/<string:council_name>')
api.add_resource(CouncilWordReviewAPI, '/api/v1/councilwords/<string:council_name>')
api.add_resource(CouncilStatsAPI, '/api/v1/councilstats/<string:council_name>')
api.add_resource(OverviewListAPI, '/api/v1/overall', endpoint = 'overviews')
api.add_resource(OverViewAPI, '/api/v1/overall/<int:id>', endpoint = 'overview')
api.add_resource(CouncilNameListAPI, '/api/v1/councilnames/')
api.add_resource(CategoriesTopFiveBottomFiveAPI, '/api/v1/categoriestopbottom/<string:category>')


if __name__ == '__main__':
    app.run(debug=True)