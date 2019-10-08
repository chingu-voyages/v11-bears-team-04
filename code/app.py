from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from db import db

from ma import ma
from security import authenticate, identity

from resources.user import UserRegister, User, UserList
from resources.invoice import Invoice, InvoiceList
from resources.team import Team, TeamList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:60a6111a8ade08958e1fb29440697522@dokku-postgres-pop-lockers:5432/pop_lockers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
app.secret_key = "hello"
api = Api(app)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity, )
api.add_resource(Invoice, '/invoice/<int:_id>')
api.add_resource(InvoiceList, '/invoices')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserList, '/users')
api.add_resource(Team, '/team/<string:business_name>')
api.add_resource(TeamList, '/teams')

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

    
# Python assigns a name to the file you run in terminal (__main__)
if __name__ == '__main__':
    ma.init_app(app)
    # this conditional will make sure this app.run only runs once
    app.run(port=8768, debug=True)  # Debug = True will display a site 4 debugging purposes
