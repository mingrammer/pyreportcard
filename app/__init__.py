from flask import Flask
from flask.ext.bower import Bower
from flask.ext.pymongo import PyMongo

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Register bower
Bower(app)

# Create mongodb client
mongo = PyMongo(app)

from .report.views import index, report