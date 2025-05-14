"""
Description: Model which represents a road.

Author: Robin
Created: 14.05.2025
Copyright: © 2025 Robin Dönnebrink
"""

from typing import Any, Final

from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry
from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, Integer, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from database import db
from models.road_network import RoadNetwork

WGS84: Final[int] = 4326  # Use World Geodetic System 84


class Road(db.Model):
    __tablename__ = "roads"

    id = Column(Integer, primary_key=True)
    road_network_id = Column(Integer, nullable=False)
    road_network_version = Column(Integer, nullable=False)
    coordinates = Column(Geometry(geometry_type="LINESTRING", srid=WGS84))
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
        coordinates: BaseGeometry,
        properties: dict[str, Any],
    ):
        self.road_network_id = road_network_id
        self.coordinates = from_shape(shape=coordinates, srid=WGS84)
        self.properties = properties
        self.road_network_version = road_network_version
        self.save()

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def to_json_obj(self):
        return {
            "type": "Feature",
            "properties": self.properties,
            "geometry": mapping(to_shape(self.coordinates)),
        }
