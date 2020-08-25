from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.user import User
from utils import hash_password


class UserListResource(Resource):

    def post(self):
        json_data = request.get_json()
        username = json_data.get('username')
        email = json_data.get('email')
        non_hashed_password = json_data.get('password')

        if User.get_by_username(username):
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
