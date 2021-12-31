import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def find_by_username(username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row is not None:
            user = User(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

    def find_by_id(_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row is not None:
            user = User(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('password', type=str, required=True,
                        help="This field cannot be left blank.")

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']) is not None:
            return {'message':'Username already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query, (data['username'],data['password']))

        connection.commit()
        connection.close()

        return {'message' : 'User created successfully.' }, 201
