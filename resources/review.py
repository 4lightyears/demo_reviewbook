from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

from models.review import Review
from schemas.review import ReviewSchema

review_schema = ReviewSchema()
review_list_schema = ReviewSchema(many=True)


class ReviewListResource(Resource):

    def get(self):
        reviews = Review.get_all()
        
        return review_list_schema.dump(reviews).data, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = review_schema.load(data=json_data)
        if errors:
            return {'message': 'Validation error', 'error': errors}, HTTPStatus.BAD_REQUEST

        review = Recipe(**data)
        review.user_id = current_user
        review.save()

        return review_schema.dump(review).data, HTTPStatus.CREATED


class ReviewResource(Resource):

    @jwt_optional
    def get(self, review_id):
        review = Review.get_by_id(review_id=review_id)

        if review is None:
            return {'message': 'review not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if review.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return review_schema.dump(review).data, HTTPStatus.OK

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