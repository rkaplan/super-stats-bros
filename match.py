from flask import Blueprint, render_template
from models import Game
from models import Player
from database import connection

match = Blueprint('match', __name__)

@match.route('/matches/<id>')
def show(id):
    game = connection['test'].games.Game.find_one({'id':int(id)})
    playerscol = connection['test'].players
    players = {}
    
    chart = {"renderTo": 'test_chart', "type": 'spline', "height": 350}
    series = []
    for p in game.players:
        players[p['player_id']] = playerscol.Player.find_one({'id':p['player_id']})
        pdata = []
        for s in game.states:
            pdata.append(s['player_states'][p['player_id']]['damage'])
        series.append({"name": str(players[p['player_id']]['name']), "data": pdata})

    plotOptions = {"series": {"marker": {"enabled": 'false'}}}
    titletext = (players[0]['name'] + ' (' + game.players[0]['character'] + ') vs. ' + players[1]['name'] + ' (' + game.players[1]['character'] + ')')
    title = {"text": str(titletext)}
    xAxis = {"title": {"text": 'Time'}, "minTickInterval": 1000, "type": 'datetime', "dateTimeLabelFormats": {"second": '%M:%S', "day": '%M:%S'}}
    yAxis = {"title": {"text": 'Damage'}, "minTickInterval": 1, "labels": {"format": '{value}%'}}
    tooltip = {"crosshairs": 'true', "shared": 'true', "xDateFormat": '%M:%S', "valueSuffix": '%'}
    
    return render_template("show.html", chart=chart, series=series, plotOptions=plotOptions, title=title, xAxis=xAxis, yAxis=yAxis, tooltip=tooltip)
