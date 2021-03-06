from db import db
# from app import ma

class TeamModel(db.Model):

    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(80))
    location = db.Column(db.String(80))

    users = db.relationship('UserModel', lazy='dynamic')

    def __init__(self, business_name, location):
        self.business_name = business_name
        self.location = location

    def json(self):
        return {
            'id': self.id,
            'business_name': self.business_name,
            'location': self.location,
            'users': [user.json() for user in self.users.all()]
        }
        # return {'business_name': self.business_name, 'users': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_business_name(cls, business_name):
        # SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(business_name=business_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
