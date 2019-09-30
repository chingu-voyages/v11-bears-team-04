from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.team import TeamModel
import datetime

class Team(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('location',
        type=str,
        required=True,
        help="Location cannot be empty"
    )

    # @jwt_required()
    def get(self, business_name):
        team = TeamModel.find_by_business_name(business_name)
        if team:
            return team.json()
            # Serialize the data for the response
            # team_schema = TeamSchema(many=True)
            # return team_schema.dump(team).data
        return {'message': 'team not found'}, 404

    # @jwt_required()
    def post(self, business_name):
        if TeamModel.find_by_business_name(business_name):
            return {'message': "That team already exists!"}

        data = Team.parser.parse_args()
        print(data['location'])
        new_team = TeamModel(business_name, data['location'])

        new_team.save_to_db()

        return new_team.json(), 201  # 201 status code means created

    def put(self, business_name):
        data = Team.parser.parse_args()

        team = TeamModel.find_by_business_name(business_name)

        if team is None:
            # team = TeamModel(name, data['price'], data['storebusiness_name'])
            team = TeamModel(**data)
        else:
            team.business_name = business_name
            team.location = data['location']

        team.save_to_db()
        return team.json()

    def delete(self, business_name):
        team = TeamModel.find_by_business_name(business_name)
        if team:
            team.delete_from_db()

        return {'message': 'team deleted'}


class TeamList(Resource):
    def get(self):
        return {'teams': list(map(lambda team: team.json(), TeamModel.query.all()))}
        # return {'teams': [team.json() for team in TeamModel.query.all()]}
