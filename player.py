from flask import Blueprint, render_template, url_for
from models import Game
from models import Player
from database import connection

player = Blueprint('player', __name__)

@player.route('/players/<id>')
def player_show(id):
    player = connection['test'].players.Player.find_one({'id':int(id)})
    gamescol = connection['test'].games
    char_games = {}
    char_wins = {}

    for g in player.games:
        game = gamescol.Game.find_one({'id':g['game_id']})
        char = ""
        for p in game.players:
            if p['player_id'] == player.id:
                char = p['character']

        if char not in char_games:
            char_games[char] = 0
            char_wins[char] = 0
        char_games[char] += 1

        if g['place'] == 0:
            if char not in char_wins:
                char_wins[char] = 0
            char_wins[char] += 1

        return render_template('player_show.html', player=player)
