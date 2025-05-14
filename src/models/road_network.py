"""
Description: Class to model a road network.

Author: Robin Dönnebrink
Created: 13.05.2025
Copyright: © 2025 Robin Dönnebrink
"""

from typing import Any

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import db


class RoadNetwork(db.Model):
    """Represents a road network system stored in a database.

    This class models a road network that consists of multiple roads associated with it. Each
    road network instance has a unique composite key consisting of an ID and a version. The
    class provides functionality for managing the lifecycle of a road network instance,
    including saving it to a database, retrieving its JSON representation, and managing versioning.

    Attributes:
        id (int): The unique identifier of the road network.
        Version (int): The version of the road network. Used in combination with `id` as a
            composite primary key.
        Owner (str): The owner of the road network.
        roads: A relationship with the `Road` model representing the collection of roads
            associated with the road network. Changes to this collection propagate to the
            database, and the deletion of the road network cascades to orphaned roads.
    """

    __tablename__ = "road_networks"

    # Combined primary key: (id, version)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    version: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    owner: Mapped[str] = mapped_column(String, nullable=False)
    roads = relationship("Road", back_populates="network", cascade="all, delete-orphan")

    def __init__(self, owner: str, _id: int | None = None):
        """Initializes an instance of a RoadNetwork.

        The owner will be assigned, and the object's unique ID as well as the initial version will be assigned.
        If a specific ID is provided, it uses that
        ID and calculates the next version number. Otherwise, it generates a new
        unique ID and starts the version at 1. The instance is then saved.

        Args:
            owner (str): The name or identifier of the owner of the instance.
            _id (int | None): An optional ID for the instance. If not provided, a new unique ID will be generated.

        Attributes:
            owner (str): Represents the owner information associated with this instance.
            id (int): A unique identifier for the instance (If not passed, a unique onw will be generated).
            version (int): The current version number of the instance (Either generated or 1).
        """
        self.owner = owner
        if _id is not None:
            self.id = _id
            self.version = self._get_next_version_number()
        else:
            self.id = RoadNetwork._get_next_id()
            self.version = 1
        self.save()

    def to_json_obj(self) -> dict[str, int | str | dict[str, Any]]:
        """Converts the instance attributes into a JSON serializable dictionary.+

        Returns: A dictionary containing the following keys:
            - id: The unique identifier of the instance.
            - version: The version of the instance.
            - owner: The owner of the instance.
            - features: A list of features assigned to this RoadNetwork.
        """
        return {
            "id": self.id,
            "version": self.version,
            "owner": self.owner,
            "features": [r.to_json_obj() for r in self.roads],
        }

    def save(self) -> None:
        """Stores this instance in the database."""
        db.session.add(self)
        db.session.commit()

    def get_max_version_number(self) -> int:
        """Determines the maximal version number of a network with this Network ID."""
        max_network = (
            RoadNetwork.query.filter(RoadNetwork.id == self.id)
            .order_by(RoadNetwork.version.desc())
            .first()
        )

        return 1 if max_network is None else max_network.version

    def _get_next_version_number(self) -> int:
        """Determines the next version number of a network with this Network ID."""
        max_network_version = self.get_max_version_number()
        return 1 if max_network_version is None else max_network_version + 1

    @staticmethod
    def _get_next_id() -> int:
        """Determines the next free RoadNetwork.ID."""
        max_network = RoadNetwork.query.order_by(RoadNetwork.id.desc()).first()
        return 1 if max_network is None else max_network.version + 1
