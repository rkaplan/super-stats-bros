from flask import Blueprint, render_template, url_for
from models import Game
from models import Player
from database import connection
from match import match
import requests
import json

index = Blueprint('index', __name__)

@index.route('/')
@index.route('/index')
def index_show():
    gamescol = connection['test'].games
    playerscol = connection['test'].players

    games = list(gamescol.Game.find())
    games = sorted(games, key=lambda g: g.end_ts)[-20:]
    players = {}
    links = {}
    for g in games:
        players[g] = []
        for p in g.players:
            players[g].append((playerscol.Player.find_one({'id':p['player_id']}).name,p['character']))
        links[g] = url_for('match.show', id=g.id)

    response = json.loads(requests.get('https://api.twitch.tv/kraken/streams/superstatsbro').content)
    online = response[unicode('stream')]
    
    return render_template('index.html', recent_games=games, players=players, links=links, response=response, online=online)
