import os

from mongokit import Connection
import models

MONGODB_URI = os.environ.get('MONGODB_URI')
connection = Connection(MONGODB_URI)

connection.register([models.Game])
connection.register([models.Player])
