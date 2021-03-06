from db import db
import datetime
import json

class InvoiceModel(db.Model):

    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80))
    phone_number = db.Column(db.String(14)) 
    amount = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    make = db.Column(db.String(80))
    model = db.Column(db.String(80))
    year = db.Column(db.Integer)
    color = db.Column(db.String(80))
    license_plate_number = db.Column(db.String(20))
    drivers_license_number = db.Column(db.String(20))
    license_state = db.Column(db.String(10))
    plate_state = db.Column(db.String(10))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def __init__(self, address, phone_number, amount, date, make, model, year, color, license_plate_number, drivers_license_number, license_state, plate_state, user_id):
        self.address = address
        self.phone_number = phone_number
        self.amount = amount
        self.date = date
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.license_plate_number = license_plate_number
        self.drivers_license_number = drivers_license_number
        self.license_state = license_state
        self.plate_state = plate_state
        self.user_id = user_id

    def json(self):
        invoice_dict = {
            'id': self.id,
            'address': self.address,
            'phone_number': self.phone_number,
            'amount': self.amount,
            'date': self.date,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'license_plate_number': self.license_plate_number,
            'drivers_license_number': self.drivers_license_number,
            'license_state': self.license_state,
            'plate_state': self.plate_state,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f"),
            'user_id': self.user_id
        }
        
        return invoice_dict

    @classmethod
    def find_by_id(cls, _id):
        # SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
