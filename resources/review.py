from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

from models.review import Review


class ReviewListResource(Resource):

    def get(self):

        reviews = Review.get_all_published()
        data = []
        for review in reviews:
            data.append(review.data())

        return {'data': data}, HTTPStatus.OK

    @jwt_required    
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        review = Review(
            rating=json_data['rating'],
            book_name=json_data['book_name'],
            body=json_data['body'],
            user_id=current_user
        )

        review.save()

        return review.data(), HTTPStatus.CREATED


class ReviewResource(Resource):

    @jwt_optional
    def get(self, review_id):
        review = Review.get_by_id(review_id=review_id)

        if review is None:
            return {'message': 'review not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if review.is_publish == False and review.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return review.data(), HTTPStatus.OK

    @jwt_required
    def put(self, review_id):
        json_data = request.get_json()

        review = Review.get_by_id(review_id=review_id)

        if review is None:
            return {'message': 'review not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if review.user_id != current_user:
            return {'message': 'Access denied'}, HTTPStatus.FORBIDDEN
        
        review.rating = json_data['rating']
        review.body = json_data['body']
        review.book_name = json_data['book_name']

        review.save()

        return review.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, review_id):
        review = Review.get_by_id(review_id=review_id)
        if review is None:
            return {'message': 'review not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if review.user_id != current_user:
            return {'message': 'Access denied'}, HTTPStatus.FORBIDDEN

        review.delete()

        return {}, HTTPStatus.NO_CONTENT


class ReviewPublishResource(Resource):

    @jwt_required
    def put(self, review_id):
        review = Review.get_all_published()

        if review is None:
            return {'message': 'review not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if review.user_id != current_user:
            return {'message': 'Access Denied.'}, HTTPStatus.FORBIDDEN

        review.is_publish = True
        review.save()

        return {}, HTTPStatus.NO_CONTENT
    
    @jwt_required
    def delete(self, review_id):
        review = Review.get_all_published()

        if review is None:
            return {'message': 'review not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if review.user_id != current_user:
            return {'message': 'Access Denied.'}, HTTPStatus.FORBIDDEN
        
        review.is_publish = False
        review.save()

        return {}, HTTPStatus.NO_CONTENT