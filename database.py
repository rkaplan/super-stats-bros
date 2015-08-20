import os

from mongokit import Connection
from models import Game

MONGODB_URI = os.environ.get('MONGODB_URI')

connection = Connection(MONGODB_URI)
connection.register([Game])

