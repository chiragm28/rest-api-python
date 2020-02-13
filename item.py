from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        required = True,
        type = float,
        help = 'This field can\'t be left blank'
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items WHERE name = ?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item':{'name': row[0], 'price':row[1]}}, 200

    @classmethod
    def insert(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(query, (item['name'], item ['price']))
        connection.commit()
        connection.close()


    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return{"message": "Item doesn\'t exist"}, 404

    def post(self, name):
        if self.find_by_name(name):
            return{'message': f"An item with the name {name} already exists."}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price'] }
        try:
            self.insert(name)
        except:
            return {"message": "An error occurred while inserting item."}, 500 #Internal Server Error
        return item, 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM items WHERE name = ?'
        cursor.execute(query,(name,))
        return{'message':"Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name':name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}
