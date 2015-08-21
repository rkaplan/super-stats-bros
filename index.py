from flask import Blueprint, render_template, url_for
from models import Game
from models import Player
from database import connection
from match import match

index = Blueprint('index', __name__)

@index.route('/')
@index.route('/index')
def index_show():
    gamescol = connection['test'].games
    playerscol = connection['test'].players

    games = list(gamescol.Game.find())
    players = {}
    links = {}
    for g in games:
        players[g] = []
        for p in g.players:
            players[g].append((playerscol.Player.find_one({'id':p['player_id']}).name,p['character']))
        links[g] = url_for('match.show', id=g.id)
    
    return render_template('index.html', recent_games=games, players=players, links=links)
