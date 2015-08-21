from flask import Blueprint, render_template, url_for
from models import Game
from models import Player
from database import connection

player = Blueprint('player', __name__)

@player.route('/players/<name>')
def player_show(name):
    player = connection['test'].players.Player.find_one({'name':name})
    playerscol = connection['test'].players
    gamescol = connection['test'].games
    char_games = {}
    char_wins = {}

    total_games = 0
    total_wins = 0
    
    chart = {"renderTo": 'test_chart', "type": 'column', "height": 350}

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
        total_games += 1

        if g['place'] == 0:
            if char not in char_wins:
                char_wins[char] = 0
            char_wins[char] += 1
            total_wins += 1

    top_char = sorted(char_games, key=char_games.__getitem__)[-5:]
            
    title = {"text": "Favorite Characters"}
    xAxis = {"categories": [str(s) for s in top_char]}
    yAxis = {"allowDecimals": 0, "minTickInterval": 1, "min": 0, "title": {"text": "Games"}}

    series = [{"name": "Games played", "color": "#0066FF", "data": [{"y": char_games[c], "name": str(c + " - " + str(char_wins[c]/char_games[c]*100)+'% winrate')} for c in top_char]}, {"name": "Wins", "color": "#009933", "data": [char_wins[c] for c in top_char]}]

    tooltip = {"shared": 1}
    plotOptions = {"series": {"pointPadding": 0}}

    recent_games = sorted([(gamescol.Game.find_one({'id':g['game_id']}), g['place']) for g in player.games], key=lambda g: g[0].end_ts)[-20:]
    players = {}
    links = {}
    for g in recent_games:
        players[g[0]] = []
        for p in g[0].players:
            players[g[0]].append((playerscol.Player.find_one({'id':p['player_id']}).name,p['character']))
        links[g[0]] = url_for('match.show', id=g[0].id)

    return render_template('player_show.html', player=player, chart=chart, series=series, plotOptions=plotOptions, title=title, xAxis=xAxis, yAxis=yAxis, tooltip=tooltip, recent_games=recent_games, players=players, links=links, total_games=total_games, total_wins=total_wins)
