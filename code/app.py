#!/usr/bin/env python3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemLists

app = Flask(__name__)
app.secret_key = 'secret'
api = Api(app)

jwt = JWT(app, authenticate, identity) # creates a new endpoint /auth

api.add_resource(ItemLists, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5002, debug=1)
