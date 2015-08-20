from flask import Flask
from flask_bootstrap import Bootstrap
from mongokit import Connection
from match import match

app = Flask(__name__)

app.register_blueprint(match)

Bootstrap(app)

if __name__ == '__main__':
    app.run(debug=True)

