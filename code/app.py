#!/usr/bin/env python3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

items = []

app = Flask(__name__)
app.secret_key = 'secret'
api = Api(app)

jwt = JWT(app, authenticate, identity) # creates a new endpoint /auth

class ItemLists(Resource):
    @jwt_required()
    def get(self):
        return {'Items': items} , 200


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('name', type=str, required=True,
                        help="This field cannot be left blank.")

    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name']==name, items),None) is not None:
            return {'message': 'Item already exists'}, 422
        requests = Item.parser.parse_args() # replacing request.get_json() which sents entire payload
        data = {'name':name, 'price': requests['price'] }
        items.append(data)
        return data, 201

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'items':item} , 200 if item is not None else 404

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'Item deleted!'}, 200

    @jwt_required()
    def put(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        requests = Item.parser.parse_args() # replacing request.get_json() which sents entire payload
        if item is not None:
            item.update(requests)
            return item, 200
        return {'message' : 'Item doesn\'t exist!'}, 404


api.add_resource(ItemLists, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

app.run(port=5002, debug=1)
