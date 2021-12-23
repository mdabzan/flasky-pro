#!/usr/bin/env python3
from flask import Flask, request
from flask_restful import Resource, Api

items = []

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)


class ItemLists(Resource):
    def get(self):
        return {'Items': items} , 200


class Item(Resource):
    def post(self, name):
        if next(filter(lambda x: x['name']==name, items),None) is not None:
            return {'message': 'Item already exists'}, 422
        requests = request.get_json()
        data = {'name':name, 'price': requests['price'] }
        items.append(data)
        return data, 201

    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'items':item} , 200 if item is not None else 404

api.add_resource(ItemLists, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=5002, debug=1)
