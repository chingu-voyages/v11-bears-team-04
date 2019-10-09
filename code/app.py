from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from db import db
import os

from ma import ma
from security import authenticate, identity

from resources.user import UserRegister, User, UserList
from resources.invoice import Invoice, InvoiceList
from resources.team import Team, TeamList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://localhost/pop-lockers')
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
    app.run(port=5000)
    # this conditional will make sure this app.run only runs once
    # app.run(port=8768, host="159.89.53.237", debug=True)  # Debug = True will display a site 4 debugging purposes
