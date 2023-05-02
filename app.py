import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__)


    # Exception occure hiden inside an extenstion of flask to propagate in main app to see it
    app.config["PROPAGATE_EXCEPTIONS"] = True
    # flask smorest configuration
    app.config["API_TITLE"] = "Stores REST API"
    #
    app.config["API_VERSION"] = "v1"
    # Standerd for API documentaion we test flask smorest to use 3.03
    app.config["OPENAPI_VERSION"] = "3.0.3"
    # to tell flask smorest where the root api is
    app.config["OPENAPI_URL_PREFIX"] = "/"
    # swagger-ui path this tell flask smorest to use swagger for api documentation 
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    # swagger-ui URL but it need to load swagger code from some were to display the documentation link of code below 
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # A connection string to our database. All database providers, such as MySQL, Postgres, 
    # PostgreeSQL, SQLite or any other use a connection string that has all the necessary 
    # information for a client to connect to the database. our Flask app is the client 
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    # slow down swlalchemy so we don't need it
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # it initializes the Flask SQLAlchemy extension, giving it our Flask app so that it can 
    # connect the Flsk app to SQLAlchemy.
    db.init_app(app)
    
    app.config["JWT_SECRET_KEY"] = "23877789178251158099025942000334528344" # secrets.SystemRandom().getrandbits(128)
    jwt = JWTManager(app)
    
    # when we expect a fresh token, but we receive a non-fresh token.
    # So that's the needs fresh token loader
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify (
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required"
                }
            )
        )
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token has been revoked",
                    "error": "token_revoked"
                }
            )
        )
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # in create_access_token we receives and identity.
        # Look in the database and see whether the user is an admin
        if  identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "message": "The token has expired.",
                    "error": "token_expired"
                }
            ),
            401,
        )
        
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Signature verification failed",
                    "error": "invalid_token"
                }
            ),
            401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required"
                }
            ),
            401,
        )

    with app.app_context():
        # it's gonna create all our tables in our database.
        db.create_all()

    # connect the flask smorest extenstion to the flask app
    api = Api(app)


    # 
    api.register_blueprint(ItemBlueprint) # these are blp varible we defined in the resources file
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app