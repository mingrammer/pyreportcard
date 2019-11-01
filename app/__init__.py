from flask import Flask

from config import Config
from flask_pymongo import PyMongo

from .report.views import about, check, index, report

app = Flask(__name__)
app.config.from_object(Config)

# Create mongodb client
mongo = PyMongo(app)
