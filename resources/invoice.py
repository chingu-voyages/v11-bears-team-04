from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.invoice import InvoiceModel
import datetime


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
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        required=False,
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

    # @jwt_required()
    def get(self, _id):
        invoice = InvoiceModel.find_by_id(_id)
        if invoice:
            return invoice.json()
        return {'message': 'Invoice not found'}, 404

    # @jwt_required()
    def post(self, _id):
        if InvoiceModel.find_by_id(_id):
            return {'message': "That invoice already exists!"}

        data = Invoice.parser.parse_args()
        new_invoice = InvoiceModel(**data)

        new_invoice.save_to_db()

        return new_invoice.json(), 201  # 201 status code means created

    def put(self, _id):
        data = Invoice.parser.parse_args()

        invoice = InvoiceModel.find_by_id(_id)

        if invoice is None:
            # invoice = InvoiceModel(name, data['price'], data['store_id'])
            invoice = InvoiceModel(**data)
        else:
            invoice.address = data['address']
            invoice.phone_number = data['phone_number']
            invoice.amount = data['amount']
            invoice.date = data['date']
            invoice.make = data['make']
            invoice.model = data['model']
            invoice.year = data['year']
            invoice.color = data['color']
            invoice.license_plate_number = data['license_plate_number']
            invoice.drivers_license_number = data['drivers_license_number']
            invoice.license_state = data['license_state']
            invoice.plate_state = data['plate_state']

        invoice.save_to_db()
        return invoice.json()

    def delete(self, _id):
        invoice = InvoiceModel.find_by_id(_id)
        if invoice:
            invoice.delete_from_db()

        return {'message': 'invoice deleted'}


class InvoiceList(Resource):
    def get(self):
        return {'invoices': list(map(lambda invoice: invoice.json(), InvoiceModel.query.all()))}
        # return {'invoices': [invoice.json() for invoice in InvoiceModel.query.all()]}
