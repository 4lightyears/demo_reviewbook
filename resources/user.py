from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_optional, jwt_required

from models.user import User
from utils import hash_password

from models.user import User
from models.review import Review

from schemas.user import UserSchema
from schemas.review import ReviewSchema

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email',))
review_list_schema = ReviewSchema(many=True)


class UserListResource(Resource):

    def post(self):
        json_data = request.get_json()
        data, errors = user_schema.load(data=json_data)
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(username=data.get('username')):
            return {'message':'username already exists.'}, HTTPStatus.BAD_REQUEST
        if User.get_by_email(email=data.get('email')):
            return {'message':'email already taken.'}, HTTPStatus.BAD_REQUEST
        
        user = User(**data)
        user.save()

        return user_schema.dump(user).data, HTTPStatus.CREATED


class UserResource(Resource):
    
    @jwt_optional
    def get(self,username):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message':'user not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user == user.id:
            user_data = user_schema.dump(user).data
        else:
            user_data = user_public_schema.dump(user).data
        
        return user_data, HTTPStatus.OK

class MeResource(Resource):
    
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        data = user_schema.dump(user).data
        return data, HTTPStatus.OK

class UserReviewListResource(Resource):
    @jwt_optional
    def get(self, username):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        
        reviews = Review.get_all_by_user(user_id=user.id)
        
        return review_list_schema.dump(reviews).data, HTTPStatus.OK