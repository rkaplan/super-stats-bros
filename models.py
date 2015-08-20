from mongokit import Document
from datetime import datetime

class Game(Document):
    structure = {
        'id': int,
        'start_ts': datetime,
        'end_ts': datetime,
        'players': [{
            'player_id': int,
            'character': basestring
        }],
        'stage_id': int,
        'states': [{
            'ts': datetime,
            'player_states': [{
                'player_id': int,
                'stock': int,
                'damage': int
            }]
        }],
        'results': [int]
    }
    use_dot_notation = True
    
class Player(Document):
    structure = {
        'id': int,
        'name': basestring,
        'games': [{
            'game_id': int,
            'place': int
        }]
    }
          
