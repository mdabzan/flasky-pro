import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

items = []

class ItemLists(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        return {'items': items}

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('name', type=str, required=True,
                        help="This field cannot be left blank.")

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item' : {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert(cls, data):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (data['name'], data['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, data):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (data['price'], data['name']))
        connection.commit()
        connection.close()

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': 'Item already exists'}, 400
        requests = Item.parser.parse_args() # replacing request.get_json() which sents entire payload
        data = {'name':name, 'price': requests['price'] }
        try:
            self.insert(data)
        except:
            return {'message': 'An error occured while inserting item.'}, 500
        return data, 201

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message' : 'Item not found'}, 404

    @jwt_required()
    def delete(self, name):
        item = self.find_by_name(name)
        if item is None:
            return {'message' : 'Item not found!'}, 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message' : 'Item deleted successfully.'}

    @jwt_required()
    def put(self, name):
        requests = Item.parser.parse_args() # replacing request.get_json() which sents entire payload
        data = {'name':name, 'price': requests['price'] }
        item = self.find_by_name(name)
        if item is not None:
            try:
                self.update(data)
            except:
                return {'message' : 'An error occured while updating item.'}, 500
            return data, 200
        return {'message' : 'Item doesn\'t exist!'}, 404
