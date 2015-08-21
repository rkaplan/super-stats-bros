from flask import Flask
from flask_bootstrap import Bootstrap
from mongokit import Connection
from match import match
from player import player
from index import index

app = Flask(__name__)

app.register_blueprint(match)
app.register_blueprint(player)
app.register_blueprint(index)

Bootstrap(app)

if __name__ == '__main__':
    app.run(debug=True)

