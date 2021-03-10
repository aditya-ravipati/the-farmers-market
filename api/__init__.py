from flask_restful import Api
from app import flaskInstance
from api.project_checkout_cart import ShoppingCart


restServer = Api(flaskInstance)
restServer.add_resource(ShoppingCart, "/api/v1.0/data")