from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

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
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://npmjs.com/package/swagger-ui-dist"

# connect the flask smorest extenstion to the flask app
api = Api(app)


#
api.register_blueprint(ItemBlueprint) # these are blp varible we defined in the resources file
api.register_blueprint(StoreBlueprint)