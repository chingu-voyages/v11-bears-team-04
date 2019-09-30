from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(30))
    phone_number = db.Column(db.String(30))
    admin = db.Column(db.Boolean)
    
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('TeamModel')

    def __init__(self, username, password, first_name, last_name, email, phone_number, admin, team_id):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.admin = admin
        self.team_id = team_id

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'admin': self.admin,
            'team_id': self.team_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
