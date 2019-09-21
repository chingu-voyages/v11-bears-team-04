from flask_restful import Resource, reqparse
from models.user import UserModel
import sqlite3


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Username cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Password cannot be blank."
    )
    parser.add_argument('email',
        type=str,
        required=True,
        help="Email cannot be blank."
    )
    parser.add_argument('first_name',
        type=str,
        required=True,
        help="First name cannot be blank."
    )
    parser.add_argument('last_name',
        type=str,
        required=True,
        help="Last name cannot be blank."
    )
    parser.add_argument('phone_number',
        type=str,
        required=True,
        help="Phone cannot be blank."
    )
    parser.add_argument('team_id',
        type=str,
        required=True,
        help="Team ID cannot be blank."
    )
    parser.add_argument('admin',
        type=bool
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)  # same as data['username'], data['password']
        user.save_to_db()

        return {"message": "User created successfully"}, 201


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Username cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Password cannot be blank."
    )
    parser.add_argument('email',
        type=str,
        required=True,
        help="Email cannot be blank."
    )
    parser.add_argument('first_name',
        type=str,
        required=True,
        help="First name cannot be blank."
    )
    parser.add_argument('last_name',
        type=str,
        required=True,
        help="Last name cannot be blank."
    )
    parser.add_argument('phone_number',
        type=str,
        required=True,
        help="Phone cannot be blank."
    )
    parser.add_argument('team_id',
        type=str,
        required=True,
        help="Team ID cannot be blank."
    )
    parser.add_argument('admin',
        type=bool
    )

    # @jwt_required()
    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404

    def put(self, username):
        data = User.parser.parse_args()

        user = UserModel.find_by_username(username)

        if user is None:
            # user = UserModel(name, data['price'], data['storeusername'])
            user = UserModel(**data)
        else:
            user.username = username
            user.password = data['password']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.phone_number = data['phone_number']
            user.team_id = data['team_id']
            user.admin = data['admin']

        user.save_to_db()
        return user.json()

    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()

        return {'message': 'user deleted'}


class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda user: user.json(), UserModel.query.all()))}
