from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not Found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'Store with {name} already exists'}

        store = StoreModel(name)
        try:
            store.save_to_db()
            return store.json(), 201
        except:
            return{'message': 'An error occured while creating the store'}, 500


    def delete(Self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return{'message': 'An error occured while deleting the store'}, 500
        return{'message':'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}


