"""
Description: Flask application for managing road networks.

Author: Robin Dönnebrink
Created: 13.05.2025
Copyright: © 2025 Robin Dönnebrink
"""

import logging
from http import HTTPStatus

import geojson
from flask import Response, abort, make_response, request
from shapely.geometry.geo import shape
from werkzeug.datastructures import FileStorage

from database import app, db
from models.road import Road  # Keep import to ensure that a table will be created
from models.road_network import RoadNetwork

logger = logging.getLogger("App")

with app.app_context():
    db.create_all()
    logger.info("Created all models successfully")


def _create_roads_for_network(
    geo_file: FileStorage, created_road_network: RoadNetwork
) -> None:
    """
    Create a set of Road based on the passed GeoJSON file for the specified RoadNetwork.

    Args:
        geo_file: valid GEOJson file.
        created_road_network: the RoadNetwork to create all the Road for.

    Raises:
        NotImplementedError: If geometry's type != LineString will be processed.

    Returns:
        None
    """
    # ToDo: Problem package rounds to precision=6 internally, but data have 7 digits.
    geo_json_data = geojson.loads(geo_file.read())
    for geo_road in geo_json_data["features"]:
        geometry_object = shape(geo_road["geometry"])
        if not geometry_object.is_valid:
            logger.info(
                f"Skip creation of road for {repr(geometry_object)} since it is not valid."
            )
            continue
        if geometry_object.geom_type != "LineString":
            raise NotImplementedError(
                f"Parsing data for {geometry_object.geom_type} is currently not implemented"
            )

        Road(
            road_network_id=created_road_network.id,
            road_network_version=created_road_network.version,
            line_geometry=geometry_object,
            properties=geo_road["properties"],
        )


# ToDo: Encapsulate geojson file checking and authorization extraction to wrapper.
@app.post("/")
def create_road_network() -> Response:
    """Creates a new RoadNetwork and all the corresponding Roads.

    Returns:
        Jsonified representation of the created RoadNetwork.
    """
    if (auth := request.form["authorization"]) is None:
        abort(HTTPStatus.BAD_REQUEST)
    elif (geo_file := request.files["file"]) is None or not geo_file.filename.endswith(
        ".geojson"
    ):
        abort(HTTPStatus.BAD_REQUEST)
    created_road_network = RoadNetwork(owner=auth)
    _create_roads_for_network(
        created_road_network=created_road_network, geo_file=geo_file
    )
    return make_response(created_road_network.to_json_obj(), HTTPStatus.CREATED)


@app.put("/<int:road_network_id>")
def update_road_network(road_network_id: int) -> Response:
    """
    Update the specified RoadNetwork by creating new Roads and marking the old as not up-to-date.
    Args:
        road_network_id: The ID of the RoadNetwork object of interest.

    Returns:
        The Jsonified representation of the RoadNetwork with the updated Roads.
    """
    if (
        road_network := RoadNetwork.query.filter(
            RoadNetwork.id == road_network_id
        ).first()
    ) is None:
        abort(HTTPStatus.NOT_FOUND)
    if (auth := request.form["authorization"]) is None:
        abort(HTTPStatus.BAD_REQUEST)
    elif (geo_file := request.files["file"]) is None or not geo_file.filename.endswith(
        ".geojson"
    ):
        abort(HTTPStatus.BAD_REQUEST)
    elif auth != road_network.owner:
        abort(HTTPStatus.UNAUTHORIZED)
    created_road_network = RoadNetwork(owner=auth, _id=road_network.id)
    _create_roads_for_network(
        created_road_network=created_road_network, geo_file=geo_file
    )
    return make_response(created_road_network.to_json_obj(), HTTPStatus.CREATED)


@app.get("/<int:road_network_id>")
def get_road_network(road_network_id: int) -> Response:
    """Returns the requested RoadNetwork either in the specified or latest version.
    Args:
        road_network_id: The ID of the RoadNetwork of interest.

    Returns:
        The Jsonified representation of the RoadNetwork either in the specified or latest version.
    """
    if (
        road_network := RoadNetwork.query.filter(
            RoadNetwork.id == road_network_id
        ).first()
    ) is None:
        abort(HTTPStatus.NOT_FOUND)
    if (auth := request.form["authorization"]) is None:
        abort(HTTPStatus.BAD_REQUEST)
    elif auth != road_network.owner:
        abort(HTTPStatus.UNAUTHORIZED)
    version = request.args.get("version")
    if version is None:
        # Use the latest version of this network
        version = road_network.get_max_version_number()
    network_of_interest = RoadNetwork.query.filter(
        RoadNetwork.id == road_network.id, RoadNetwork.version == version
    ).one()
    return make_response(network_of_interest.to_json_obj(), HTTPStatus.OK)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
