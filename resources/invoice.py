from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.invoice import InvoiceModel


class Invoice(Resource):
    #parser makes sure that the price argument is included in the request
    parser = reqparse.RequestParser()
    parser.add_argument('address',
        type=str,
        required=True,
        help="Address cannot be left blank"
    )
    parser.add_argument('phone_number',
        type=str,
        required=True,
        help="Phone cannot be left blank"
    )
    parser.add_argument('amount',
        type=int,
        required=True,
        help="Amount cannot be left blank"
    )
    parser.add_argument('date',
        type='date', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        required=True,
        help="Date cannot be left blank"
    )
    parser.add_argument('make',
        type=str,
        required=True,
        help="Make cannot be left blank"
    )
    parser.add_argument('model',
        type=str,
        required=True,
        help="Model cannot be left blank"
    )
    parser.add_argument('year',
        type=int,
        required=True,
        help="Year cannot be left blank"
    )
    parser.add_argument('color',
        type=str,
        required=True,
        help="Color cannot be left blank"
    )
    parser.add_argument('license_plate_number',
        type=str,
        required=True,
        help="License plate # cannot be left blank"
    )
    parser.add_argument('drivers_license_number',
        type=str,
        required=True,
        help="Drivers license # cannot be left blank"
    )
    parser.add_argument('license_state',
        type=str,
        required=True,
        help="License state cannot be left blank"
    )
    parser.add_argument('plate_state',
        type=str,
        required=True,
        help="Plate state cannot be left blank"
    )

    @jwt_required()
    def get(self, id):
        item = InvoiceModel.find_by_id(id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    # @jwt_required()
    def post(self, id):
        if InvoiceModel.find_by_id(id):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        # request_data = request.get_json() # you don't need content-type header with force=True
        new_item = InvoiceModel(name, data['price'], data['store_id'])

        try:
            new_item.save_to_db()
        except:
            return{"message": "An error happened inserting the item."}, 500

        return new_item.json(), 201  # 201 status code means created

    def put(self, id):
        data = Item.parser.parse_args()

        item = InvoiceModel.find_by_id(id)

        if item is None:
            # item = InvoiceModel(name, data['price'], data['store_id'])
            item = InvoiceModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()

    def delete(self, id):
        item = InvoiceModel.find_by_id(id)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda item: item.json(), InvoiceModel.query.all()))}
        # return {'items': [item.json() for item in InvoiceModel.query.all()]}
