"""
Description: Flask application for managing road networks.

Author: Robin Dönnebrink
Created: 13.05.2025
Copyright: © 2025 Robin Dönnebrink
"""

import json
import logging
from http import HTTPStatus

from flask import abort, make_response, request
from shapely.geometry.geo import shape

from database import app, db
from models.road import Road  # Keep import to ensure that table will be created
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
    elif (geo_file := request.files["file"]) is None or not geo_file.filename.endswith(
        ".geojson"
    ):
        abort(400)
    created_road_network = RoadNetwork(owner=auth)
    logger.error("!!!!!!!!!")
    import geojson

    geo_json_data = geojson.loads(geo_file.read())
    for geo_road in geo_json_data["features"]:
        geometry_data = geo_road["geometry"]
        logger.error("!!!!!!")
        logger.error(geometry_data)
        shape_geometry = shape(geo_road["geometry"])
        if not shape_geometry.is_valid:
            continue
        if shape_geometry.geom_type != "LineString":
            raise NotImplementedError(
                f"Parsing data for {shape_geometry.geom_type} is currently not implemented"
            )

        Road(
            road_network_id=created_road_network.id,
            coordinates=shape_geometry,
            properties=geo_road["properties"],
        )
    return make_response(created_road_network.to_json_obj(), HTTPStatus.CREATED)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
