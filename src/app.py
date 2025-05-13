"""
Description: Flask application for managing road networks.

Author: Robin Dönnebrink
Created: 13.05.2025
Copyright: © 2025 Robin Dönnebrink
"""

from database import app, db
from models.road_network import RoadNetwork
import logging

logger = logging.getLogger("App")

with app.app_context():
    db.create_all()
    logger.info("Created all models successfully")



@app.route("/")
def hello():
    return RoadNetwork.query.all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
