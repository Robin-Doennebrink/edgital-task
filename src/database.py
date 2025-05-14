"""
Description: Set up the connection of SQLAlchemy to the postgres database.

Author: Robin
Created: 13.05.2025
Copyright: © 2025 Robin Dönnebrink
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Get the database URL from the environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)
