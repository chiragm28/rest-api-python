import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        required = True,
        type = float,
        help = 'This field can\'t be left blank'
    )

    parser.add_argument('store_id',
        required = True,
        type = int,
        help = 'Every item needs a store id'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return{"message": "Item doesn\'t exist"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return{'message': f"An item with the name {name} already exists."}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting item."}, 500 #Internal Server Error
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return{'message':"Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item_.json() for item_ in ItemModel.query.all()]}
