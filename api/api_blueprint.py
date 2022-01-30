from flask import Blueprint
from flask_restful import Api, Resource

from api.auth.resource import LoginResource
from api.prediction.resource import DataSaverResource, UserSeederResource, RecommendedProductResource, \
    PopularProductResource

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)
api.add_resource(LoginResource, '/auth/login')
api.add_resource(DataSaverResource, '/seed-recommended-products')
api.add_resource(UserSeederResource, '/seed-users')
api.add_resource(PopularProductResource, '/popular-products')
api.add_resource(RecommendedProductResource, '/users/<user_id>/recommended-products')
