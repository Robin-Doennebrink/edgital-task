"""
Description: Class to model a road network.

Author: Robin Dönnebrink
Created: 13.05.2025
Copyright: © 2025 Robin Dönnebrink
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import db


class RoadNetwork(db.Model):
    __tablename__ = "road_networks"

    # Combined primary key: (id, version)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    version: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    owner: Mapped[str] = mapped_column(String, nullable=False)
    roads = relationship("Road", back_populates="network", cascade="all, delete-orphan")

    def __init__(self, owner: str, _id: int | None = None):
        self.owner = owner
        if _id is not None:
            self.id = _id
            self.version = self._get_next_version_number()
        else:
            self.id = RoadNetwork._get_next_id()
            self.version = 1
        self.save()

    def to_json_obj(self) -> dict[str, int | str | dict]:
        return {
            "id": self.id,
            "version": self.version,
            "owner": self.owner,
            "features": [r.to_json_obj() for r in self.roads],
        }

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def get_max_version_number(self) -> int:
        max_network = (
            RoadNetwork.query.filter(RoadNetwork.id == self.id)
            .order_by(RoadNetwork.version.desc())
            .first()
        )

        return 1 if max_network is None else max_network.version

    def _get_next_version_number(self) -> int:

        max_network_version = self.get_max_version_number()
        return 1 if max_network_version is None else max_network_version + 1

    @staticmethod
    def _get_next_id():
        max_network = RoadNetwork.query.order_by(RoadNetwork.id.desc()).first()
        return 1 if max_network is None else max_network.version + 1
