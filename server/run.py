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

        #replace white space
        for k,v in query.items():
            k = k.replace("%20", " ")
            query[k] = v.replace("%20", " ")

        for k,v in query.items():
            if "__" in v:
                query[k] = {v.split("__")[0]:v.split("__")[1]}
        print(query)
        cursor = db.overall.find(query)
        json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
        return json_docs

class OverViewAPI(Resource):
    def get(self, id):
        db.overall.find({"FHSID":id})




api.add_resource(OverviewListAPI, '/api/v1/overall', endpoint = 'overviews')
api.add_resource(OverViewAPI, '/api/v1/overall/<int:id>', endpoint = 'overview')

if __name__ == '__main__':
    app.run(debug=True)