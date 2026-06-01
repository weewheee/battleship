from packages import *
import flask
import json

# set ships in known positions for testing purposes
TESTING = True
TESTING_SHIP_POSITIONS = [
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)], 
    [(2, 0), (2, 1), (2, 2), (2, 3)], 
    [(4, 0), (4, 1), (4, 2)], 
    [(6, 0), (6, 1), (6, 2)], 
    [(8, 0), (8, 1)] 
]
ai_board = Board()
player_board = Board()

set_ships: bool = True
ship_positions: list = []

winner = ''

# function to reset all game variables to their initial state
def reset():
    global ai_board, player_board, set_ships, ship_positions, winner
    ai_board = Board()
    player_board = Board()
    set_ships = True
    ship_positions = []
    winner = None

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

# Redirect page to ensure that the game state is reset when the player clicks the "Play" button on the index page
@app.route('/redirect')
def redirect():
    reset()
    return flask.redirect('/play')

@app.route('/play')
def play():
    # Let player set ship positions first
    global set_ships
    if set_ships:
        return flask.render_template('set_ship.html')
    
    # If player has set ship positions, start the game
    context = {
        'ai_board': ai_board.grid.tolist(),
        'player_board': player_board.grid.tolist(),
        'ship_placements': ship_positions,
        'winner': winner
    }
    return flask.render_template('game_board.html', **context)

@app.route('/play/set-ships', methods=['POST'])
def play_set_ships():
    global ship_positions, set_ships

    # Get ship placements from the request body and store them in the global variable
    ship_positions = flask.request.json['ship_placements']
    set_ships = False

    # Set ships on player and ai boards
    if TESTING:
        ai_board.set_ships(*TESTING_SHIP_POSITIONS)
    else:
        ai_board.set_ships()

    player_ship_positions = []
    # Convert positions in list from list to tuple
    for ship in ship_positions:
        positions = [tuple(pos) for pos in ship['positions']]
        player_ship_positions.append(positions)

    player_board.set_ships(*player_ship_positions)

    print(set_ships)
    return flask.jsonify({'success': True})

@app.route('/play/player-move', methods=['POST'])
def player_move():
    row, col = flask.request.json['row'], flask.request.json['col']

    # Register the player's move on the AI's board and return whether it was a hit or miss
    hit, sink_positions = ai_board.receive_attack((row, col))

    # Change tuples in sink_positions to lists for JSON serialization
    sink_positions = [list(pos) for pos in sink_positions]
    sink_positions.sort()

    # Set winner variable if game is won by player
    global winner
    if all(ship.sunk for ship in ai_board.ships):
        print('player win')
        winner = 'player'

    # Return game state as JSON to html
    response  = {
        'hit': hit,
        'sinkPositions': sink_positions,
        'winner': winner,
        'winStats': {
            'hitCount': ai_board.hit_count,
            'missCount': ai_board.miss_count,
            'totalAttacks': ai_board.hit_count + ai_board.miss_count
        }
    }
    return flask.jsonify(response)

@app.route('/play/ai-move', methods=['POST'])
def ai_move():
    # AI makes a move on the player's board and return whether it was a hit or miss
    next_move = ai.generate_next_move(player_board.grid, [ship.sunk for ship in player_board.ships])
    hit, sink_positions = player_board.receive_attack(next_move)

    # Change tuples in sink_positions to lists for JSON serialization
    sink_positions = [list(pos) for pos in sink_positions]
    sink_positions.sort()

    # Set winner variable if game is won by AI
    global winner
    if all(ship.sunk for ship in player_board.ships):
        winner = 'ai'

    # Return game state as JSON to html
    response  = {
        'row': next_move[0],
        'col': next_move[1],        
        'hit': hit,
        'sinkPositions': sink_positions,
        'winner': winner,
        'winStats': {
            'hitCount': player_board.hit_count,
            'missCount': player_board.miss_count,
            'totalAttacks': player_board.hit_count + player_board.miss_count
        }
    }
    return flask.jsonify(response)

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()