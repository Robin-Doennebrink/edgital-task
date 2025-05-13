"""
Description: [Add module purpose here]

Author: Robin
Created: 13.05.2025
Copyright: © 2025 Robin Dönnebrink
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Get the database URL from the environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)
