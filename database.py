from mongokit import Connection
import models

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

connection = Connection(MONGODB_HOST, MONGODB_PORT)
connection.register([models.Game])
connection.register([models.Player])
