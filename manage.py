import os
import unittest
from flask import Flask, jsonify, make_response
from flask.cli import FlaskGroup
from app.main import create_app, db
from flask_migrate import Migrate
from app.main.model import models
from app import blueprint
from flask_cors import CORS
import logging
from werkzeug.exceptions import HTTPException



UPLOAD = 'uploaded-files/'
IMG_UPLOAD = 'static/assets/images/'

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret_key')

app.app_context().push()


print(f"Configured JWT_SECRET_KEY: {app.config['JWT_SECRET_KEY']}")

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_dir):
   os.makedirs(log_dir)

app.config['LOG_FOLDER'] = log_dir

CORS(app)
Migrate(app, db)

cli = FlaskGroup(app)


# we will do this for each custom exception class for ERROR_CODE_INVALID_FORMAT
class InvalidFormatException(HTTPException):
    code = 1001  # HTTP status code
    description = "The uploaded file has an unsupported format."


@app.route("/health")
def health_check():
    """try:
        data = ChatsTable.query.all()
        return jsonify({"status": 200})
    except Exception as e:
        # If any check fails, return an error message with a status code of 500"""
    return jsonify({"status": 200})


@app.route("/")
def home():
    """db.session.query(ParsonalFilesAnalysisTable).delete()
    db.session.commit()
    print("delete")"""
    #socketio.emit('progress', {'progress': 100}, namespace='/progress')
    return jsonify({"massege": "Add /ais/ to get the endpoints"})
     
# Custom Error Handler for InvalidFormatException
@app.errorhandler(InvalidFormatException)
def invalid_format_error_handler(e):
    # Create a response object will be imported from the custom error codes in the utils 
    error_response = {
        "error_code": e.code,
        "error_name": e.error_name,
        "error_message": e.description,
    }
    
    # Return the response as JSON with the appropriate status code
    return jsonify(error_response), e.code


@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)

"""
@app.errorhandler(500)
def handle_500_error(_error):
   "Return a http 500 error to client"
    return make_response(jsonify({'error': 'Server error'}), 500)

"""
@cli.command("run")
def run():
    del os.environ["FLASK_RUN_FROM_CLI"]
    app.run(host="0.0.0.0", port=5001, debug=True)

@cli.command("db_create_all")
def db_create_all():
    """Initialize the database."""
    db.create_all()


@cli.command("test")
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    cli()
