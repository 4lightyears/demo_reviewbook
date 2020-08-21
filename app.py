from flask import Flask
from flask_restful import Api

from resources.review import ReviewListResource, ReviewResource, ReviewPublishResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ReviewListResource, '/reviews')
api.add_resource(ReviewResource, '/reviews/<int:review_id>')
api.add_resource(ReviewPublishResource, '/reviews/<int:review_id>/publish')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

