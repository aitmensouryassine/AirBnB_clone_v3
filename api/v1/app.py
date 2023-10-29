#!/usr/bin/python3
"""start a flask application on 0.0.0.0 port 5000"""

from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
import json
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(ret):
    """Calls storage.close method"""
    storage.close()


@app.errorhandler(404)
def notFoundHandler(err):
    """To handler the error 404 :Not found"""
    error_msg = {"error": "Not found"}
    response = make_response(json.dumps(error_msg), 404)
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    """start application on 0.0.0.0:5000"""
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
