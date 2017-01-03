from flask import Flask, request
from flask_restful import Resource, Api
from src.db.connection import DbConnection
from bson import json_util
import json

app = Flask(__name__)
api = Api(app)
db = DbConnection().get_restaurant_db()

todos = {}

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
        return json_docs

api.add_resource(CouncilWordReviewAPI, '/api/v1/councilwords/<string:council_name>')
api.add_resource(CouncilStatsAPI, '/api/v1/councilstats/<string:council_name>')
api.add_resource(OverviewListAPI, '/api/v1/overall', endpoint = 'overviews')
api.add_resource(OverViewAPI, '/api/v1/overall/<int:id>', endpoint = 'overview')
api.add_resource(CouncilNameListAPI, '/api/v1/councilnames/')


if __name__ == '__main__':
    app.run(debug=True)