"""
Description: Flask application for managing road networks.

Author: Robin Dönnebrink
Created: 13.05.2025
Copyright: © 2025 Robin Dönnebrink
"""

import logging
from http import HTTPStatus

from flask import abort, make_response, request

from database import app, db
from models.road_network import RoadNetwork

logger = logging.getLogger("App")

with app.app_context():
    db.create_all()
    logger.info("Created all models successfully")


@app.route("/")
def hello():
    return RoadNetwork.query.all()


@app.post("/")
def create_road_network():
    if (auth := request.form["authorization"]) is None:
        abort(400)
    elif (geo_file := request.files["file"]) is None:
        abort(400)
    created_road_network = RoadNetwork(owner=auth)
    return make_response(created_road_network.to_json_obj(), HTTPStatus.CREATED)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
