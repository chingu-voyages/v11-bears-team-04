from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Invoice(Resource):
    #parser makes sure that the price argument is included in the request
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    # @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        #42-43 same as 45-46, with helper function
        # if next(filter(lambda ite: ite['name'] == name, items), None):
        #     return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        # request_data = request.get_json() # you don't need content-type header with force=True
        new_item = ItemModel(name, data['price'], data['store_id'])

        try:
            new_item.save_to_db()
        except:
            return{"message": "An error happened inserting the item."}, 500

        return new_item.json(), 201  # 201 status code means created

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda item: item.json(), ItemModel.query.all()))}
        # return {'items': [item.json() for item in ItemModel.query.all()]}
