"""
Description: Model which represents a road.

Author: Robin Dönnebrink
Created: 14.05.2025
Copyright: © 2025 Robin Dönnebrink
"""

from typing import Any, Final

from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry
from sqlalchemy import Column, ForeignKeyConstraint, Integer
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from database import db

WGS84: Final[int] = 4326  # Use World Geodetic System 84


class Road(db.Model):
    """Model which represents a Road of a RoadNetwork with the following attributes:

    - id: The primary key
    - road_network_id: Stores the ID of the RoadNetwork it belongs to.
    - road_network_version: Stores the version of the RoadNetwork it belongs to.
    - line_geometry: The geospatial data of this Road.
    - properties: Additional properties to store for this Route.

    """

    __tablename__ = "roads"

    id = Column(Integer, primary_key=True)
    road_network_id = Column(Integer, nullable=False)
    road_network_version = Column(Integer, nullable=False)
    line_geometry = Column(Geometry(geometry_type="LINESTRING", srid=WGS84))
    properties = Column(JSON, nullable=False)

    network = relationship("RoadNetwork", back_populates="roads")
    # Composite foreign key constraint for RoadNetwork entity.
    __table_args__ = (
        ForeignKeyConstraint(
            ["road_network_id", "road_network_version"],
            ["road_networks.id", "road_networks.version"],
            name="fk_road_network",
        ),
    )

    def __init__(
        self,
        road_network_id: int,
        road_network_version: int,
        line_geometry: BaseGeometry,
        properties: dict[str, Any],
    ):
        """
        Creates and saves a new Road to the database.

        Args:
            road_network_id: The ID of the RoadNetwork it belongs to.
            road_network_version:  the version of the RoadNetwork it belongs to.
            line_geometry:  The geospatial data of this Road.
            properties: Additional properties to store for this Route.
        """
        self.road_network_id = road_network_id
        self.line_geometry = from_shape(shape=line_geometry, srid=WGS84)
        self.properties = properties
        self.road_network_version = road_network_version
        self.save()

    def save(self) -> None:
        """
        Saves the new Road object to the database.
        """
        db.session.add(self)
        db.session.commit()

    def to_json_obj(self) -> dict[str, str | dict[str, Any]]:
        """Returns a JSON representation of the Road object.

        Returns:
            a dictionary representing this Road as a GEOJson object.
        """
        return {
            "type": "Feature",
            "properties": self.properties,
            "geometry": mapping(to_shape(self.line_geometry)),
        }
