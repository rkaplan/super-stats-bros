from flask import Blueprint, render_template, url_for
from models import Game
from models import Player
from database import connection
from player import player

match = Blueprint('match', __name__)

@match.route('/matches/<id>')
def show(id):
    game = connection['test'].games.Game.find_one({'id':int(id)})
    playerscol = connection['test'].players
    players = {}
    
    chart = {"renderTo": 'test_chart', "type": 'spline', "height": 350}
    series = []
    currcolor = 0
    colors = ['#009933', '#0066FF', '#CC0000', '#9900FF']
    shapes = ['circle', 'square', 'triangle', 'diamond']
    for p in game.players:
        players[p['player_id']] = playerscol.Player.find_one({'id':p['player_id']})
        ko = []
        pdata = []
        prev = -1
        ps = game.states[0]
        first = True
        for s in game.states:
            stock = s['player_states'][p['player_id']]['stock']
            if s != game.states[0] and stock != prev:
                ko.append(ps)
            prev = stock
            ps = s
        for s in game.states:
            time = s['ts']-game['start_ts']
            if s not in ko:
                pdata.append({'x': time.seconds*1000 - time.microseconds/1000, 'y': s['player_states'][p['player_id']]['damage'], 'marker': {'symbol': shapes[currcolor]}})
            else:
                pdata.append({'x': time.seconds*1000 - time.microseconds/1000, 'y': s['player_states'][p['player_id']]['damage'], 'marker': {'enabled': 1, 'symbol': 'url(' + url_for('static', filename='explosion.png') + ')'}})
                if first:
                    series.append({"name":str(players[p['player_id']]['name']), "data": pdata, "color": colors[currcolor]})
                else:
                    series.append({"name":str(players[p['player_id']]['name']), "data": pdata, "linkedTo": ":previous", "color": colors[currcolor]})
                first = False
                pdata = []
        if first:
            series.append({"name":str(players[p['player_id']]['name']), "data": pdata, "color": colors[currcolor]})
        else:
            series.append({"name":str(players[p['player_id']]['name']), "data": pdata, "linkedTo": ":previous", "color": colors[currcolor]})
        currcolor += 1
        #series.append({"name": str(players[p['player_id']]['name']), "data": pdata})

    plotOptions = {"series": {"marker": {"enabled": 0}}}
    titletext = (players[0]['name'] + ' (' + game.players[0]['character'] + ') vs. ' + players[1]['name'] + ' (' + game.players[1]['character'] + ')')
    title = {"text": str(titletext)}
    xAxis = {"title": {"text": 'Time'}, "minTickInterval": 1000, "type": 'datetime', "dateTimeLabelFormats": {"second": '%M:%S', "day": '%M:%S'}}
    yAxis = {"title": {"text": 'Damage'}, "minTickInterval": 1, "labels": {"format": '{value}%'}, "min": 0}
    tooltip = {"crosshairs": 1, "shared": 1, "xDateFormat": '%M:%S', "valueSuffix": '%'}

    playernames = []
    links = {}
    for r in game.results:
        playernames.append(players[r].name)
        links[players[r].name] = url_for('player.player_show',name=str(players[r].name))
    places = {}
    for p in game.players:
        places[players[p['player_id']].name] = p['character']
        
    return render_template("show.html", chart=chart, series=series, plotOptions=plotOptions, title=title, xAxis=xAxis, yAxis=yAxis, tooltip=tooltip, playernames=playernames, places=places, links=links, id=id)
