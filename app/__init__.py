from flask_restx import Api
from flask import Blueprint


from .main.controller.content_controller import api as content_ns




blueprint = Blueprint('api_v1', __name__, url_prefix='/ais')
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    
    blueprint,
    title='Assistant AI API enpoints',
    version='3.0.0',
    description='Assistant AI endpoints',
    authorizations=authorizations,
    security='apikey',
    default_mediatype='multipart/form-data',
   
    license =  {
      "name": "Assistant",
      "url": "https://opensource.org/licenses/MIT"
    },
    tags = [
    {
      "name": "Assistant AI APIs",
      "description": "Assistant backend API endpoints"
    }
  ],
)


api.add_namespace(content_ns)

