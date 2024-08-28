from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchema, ItemGetSchema, ItemOptionalQuerySchema, ItemQuerySchema, SucessMessageSchema
from uuid import uuid4

blp = Blueprint('items', __name__, description="Operations on items")

@blp.route('/item')
class Item(MethodView):  # Changed class name to avoid conflict with variable 'items'
    @blp.response(200, ItemGetSchema(many = True))
    @blp.arguments(ItemOptionalQuerySchema, location = 'query')
    def get(self, args):
        id = args.get('id')
        if id is None:
            return items

        for curr in items:
            if curr['id'] == id: 
                return [curr]
        abort(404, message = 'This item does not exist')

    @blp.arguments(ItemSchema)
    @blp.response(200, SucessMessageSchema)
    @blp.arguments(ItemQuerySchema, location = 'query')
    def put(self, request_data, args):
        id = args.get('id')
        for item in items:
            if item['id'] == id:
                item['item']['price'] = request_data['price']
                return {'message': 'Item updated successfully'}, 200

        return {'message': 'The item does not exist'}, 404

    @blp.arguments(ItemSchema)
    @blp.response(200, SucessMessageSchema)
    def post(self, request_data):
        item = {}
        item['id'] = uuid4().hex
        item['item'] = {}
        item['item']['name'] = request_data['name']
        item['item']['price'] = request_data['price']
        items.append(item)
        return {"message": "Item added successfully"}, 201

    @blp.response(200, SucessMessageSchema)
    @blp.arguments(ItemQuerySchema, location = 'query')
    def delete(self, args):
        id = args.get('id')
        for item in items:
            if item['id'] == id:
                items.remove(item)
                return {'message': 'Item removed successfully'}, 200

        return {'message': 'Item does not exist'}, 404
