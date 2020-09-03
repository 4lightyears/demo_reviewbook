from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.user import User
from utils import hash_password
from flask_jwt_extended import get_jwt_identity, jwt_optional, jwt_required


class UserListResource(Resource):

    def post(self):
        json_data = request.get_json()
        username = json_data.get('username')
        email = json_data.get('email')
        non_hashed_password = json_data.get('password')

        if User.get_by_username(username=username):
            return {'message':'username already exists.'}, HTTPStatus.BAD_REQUEST
        if User.get_by_email(email):
            return {'message':'email already taken.'}, HTTPStatus.BAD_REQUEST
        
        hashed_password = hash_password(non_hashed_password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        user.save()

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        return data, HTTPStatus.CREATED


class UserResource(Resource):
    
    @jwt_optional
    def get(self,username):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message':'user not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user == user.id:
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }, HTTPStatus.OK
        else:
            return {
                'id': user.id,
                'username': user.username
            }, HTTPStatus.OK


class MeResource(Resource):
    
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        
        data = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        }

        return data, HTTPStatus.OK
