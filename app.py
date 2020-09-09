from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from resources.user import UserListResource, UserResource, MeResource, UserReviewListResource
from resources.review import ReviewListResource, ReviewResource
from resources.token import TokenResource, RefreshResource, RevokeResource, black_list

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
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app) 

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        
        return jti in black_list


def register_resource(app):
    api = Api(app)
    api.add_resource(ReviewListResource, '/reviews')
    api.add_resource(ReviewResource, '/reviews/<int:review_id>')

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')
    api.add_resource(UserReviewListResource, '/users/<string:username>/reviews')
    
    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

if __name__ == '__main__':
    app = create_app()
    app.run()