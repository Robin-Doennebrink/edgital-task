"""
Description: Class to model a road network.

Author: Robin Dönnebrink
Created: 13.05.2025
Copyright: © 2025 Robin Dönnebrink
"""

from sqlalchemy import  String
from sqlalchemy.orm import Mapped, mapped_column

from database import db

class RoadNetwork(db.Model):
    __tablename__  = "road_network"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped[str] = mapped_column(String)

