from flask import Blueprint, render_template
from models import Game
from database import connection

match = Blueprint('match', __name__)

@match.route('/matches/<id>')
def show(id):
    game = connection['test'].games.Game.find_one({'id':int(id)})
    
    chart = {"renderTo": 'test_chart', "type": 'spline', "height": 350}
    series = []
    for p in game.players:
        pdata = []
        for s in game.states:
            pdata.append(s['player_states'][p['player_id']]['damage'])
        series.append({"name": 'Player ' + str(p['player_id']), "data": pdata})

    plotOptions = {"series": {"marker": {"enabled": 'false'}}}
    title = {"text": 'My Title'}
    xAxis = {"title": {"text": 'Time'}, "minTickInterval": 1000, "type": 'datetime', "dateTimeLabelFormats": {"second": '%M:%S', "day": '%M:%S'}}
    yAxis = {"title": {"text": 'Damage'}, "minTickInterval": 1, "labels": {"format": '{value}%'}}
    tooltip = {"crosshairs": 'true', "shared": 'true', "xDateFormat": '%M:%S', "valueSuffix": '%'}
    
    return render_template("show.html", chart=chart, series=series, plotOptions=plotOptions, title=title, xAxis=xAxis, yAxis=yAxis, tooltip=tooltip)
