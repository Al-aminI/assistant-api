from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from .config import config_by_name
import os

#from app import api
db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    """Create a Flask application with the given configuration name.

    Args:
        config_name (str): The name of the configuration to use.

    Returns:
        Flask: The Flask application.

    """
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 5000 * 1024 * 1024 
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret_key')
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    

    #api.init_app(app)
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app