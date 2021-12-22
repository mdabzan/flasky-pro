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
        items.append(data)
        return data, 201

    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item, 200
        return {'item': None}, 404


api.add_resource(ItemLists, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=5002, debug=1)
