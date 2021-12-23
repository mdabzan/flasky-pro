#!/usr/bin/env python3
from flask import Flask, request
from flask_restful import Resource, Api

items = []

app = Flask(__name__)
api = Api(app)


class ItemLists(Resource):
    def get(self):
        return {'Items': items} , 200


class Item(Resource):
    def post(self, name):
        requests = request.get_json()
        data = {'name':name, 'price': requests['price'] }
        if data not in items:
            items.append(data)
            return data, 201
        else:
            return {'message': 'Item already exists'}, 422

    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'items':item} , 200 if item is not None else 404

api.add_resource(ItemLists, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=5002, debug=1)
