#!/usr/bin/python3
"""Index view file"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """Display the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """Display the stats"""
    from models.user import User
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.state import State
    from models.review import Review
    from models import storage

    stats_data = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return stats_data
