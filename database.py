from mongokit import Connection
from models import Game

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

connection = Connection(MONGODB_HOST, MONGODB_PORT)
connection.register([Game])

