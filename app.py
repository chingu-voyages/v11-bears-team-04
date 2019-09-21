from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from resources.user import UserRegister, User, UserList
from resources.invoice import Invoice, InvoiceList
from resources.team import Team, TeamList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pop-lockers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "hello"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)
# api.add_resource(Invoice, '/invoice')
api.add_resource(Invoice, '/invoice/<int:_id>')
api.add_resource(InvoiceList, '/invoices')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserList, '/users')
api.add_resource(Team, '/team/<string:business_name>')
api.add_resource(TeamList, '/teams')

# Python assigns a name to the file you run in terminal (__main__)
if __name__ == '__main__':
    from db import db
    # this conditional will make sure this app.run only runs once
    db.init_app(app)
    app.run(port=5000, debug=True)  # Debug = True will display a site for debugging
