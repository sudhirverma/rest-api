from flask import Flask
from flask_smorest import Api
import os

import models

from db import db
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

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

    with app.app_context():
        # it's gonna create all our tables in our database.
        db.create_all()

    # connect the flask smorest extenstion to the flask app
    api = Api(app)


    # 
    api.register_blueprint(ItemBlueprint) # these are blp varible we defined in the resources file
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app