"""
Description: Class to model a road network.

Author: Robin Dönnebrink
Created: 13.05.2025
Copyright: © 2025 Robin Dönnebrink
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import db


class RoadNetwork(db.Model):
    __tablename__ = "road_network"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    owner: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(self, owner: str):
        self.owner = owner
        self.save()

    def to_json_obj(self) -> dict[str, int | str]:
        return {"id": self.id, "owner": self.owner}

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
