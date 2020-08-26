from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from resources.user import UserListResource, UserResource, MeResource
from resources.review import ReviewListResource, ReviewResource, ReviewPublishResource
from resources.token import TokenResource

from config import Config
from models.user import User
from extensions import db, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extension(app)
    register_resource(app)

    return app

def register_extension(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

def register_resource(app):
    api = Api(app)
    api.add_resource(ReviewListResource, '/reviews')
    api.add_resource(ReviewResource, '/reviews/<int:review_id>')
    api.add_resource(ReviewPublishResource, '/reviews/<int:review_id>/publish')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')
    api.add_resource(TokenResource, '/token')


if __name__ == '__main__':
    app = create_app()
    app.run()

