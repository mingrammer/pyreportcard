from flask import Flask
from flask_pymongo import PyMongo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Create mongodb client
mongo = PyMongo(app)

from .report.views import *  # flake8: noqa
