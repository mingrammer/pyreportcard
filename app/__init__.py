from flask import Flask
from flask_bower import Bower
from flask_pymongo import PyMongo

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Register bower
Bower(app)

# Create mongodb client
mongo = PyMongo(app)

from .report.views import index, report