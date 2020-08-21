from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.review import Review, review_list


class ReviewListResource(Resource):

    def get(self):

        data = []

        for review in review_list:
            if review.is_publish is True:
                data.append(review.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        review = Review(
            rating=data['rating'],
            book_name=data['book_name'],
            body=data['body']
        )

        review_list.append(review)

        return review.data, HTTPStatus.CREATED


class ReviewResource(Resource):

    def get(self, review_id):
        review = next((review for review in review_list if review.id == review_id and review.is_publish == True), None)

        if review is None:
            return {'message': 'review not found'}, HTTPStatus.NOT_FOUND

        return review.data, HTTPStatus.OK

    def put(self, review_id):
        data = request.get_json()

        review = next((review for review in review_list if review.id == review_id), None)

        if review is None:
            return {'message': 'review not found'}, HTTPStatus.NOT_FOUND

        review.rating = data['rating']
        review.body = data['body']
        review.book_name = data['book_name']

        return review.data, HTTPStatus.OK

    def delete(self, review_id):
        review = next((review for review in review_list if review.id == review_id), None)

        if review is None:
            return {'message': 'review not found'}, HTTPStatus.NOT_FOUND

        review_list.remove(review)

class ReviewPublishResource(Resource):

    def put(self, review_id):
        review = next((review for review in review_list if review.id == review_id), None)

        if review is None:
            return {'message': 'review not found'}, HTTPStatus.NOT_FOUND

        review.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, review_id):
        review = next((review for review in review_list if review.id == review_id), None)

        if review is None:
            return {'message': 'review not found'}, HTTPStatus.NOT_FOUND

        review.is_publish = False

        return {}, HTTPStatus.NO_CONTENT