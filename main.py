from packages import *
import flask
import json

# set ships in known positions for testing purposes
testing_ship_positions = [
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

# function to reset all game variables to their initial state
def reset():
    global ai_board, player_board, set_ships, ship_positions
    ai_board = Board()
    player_board = Board()
    set_ships = True
    ship_positions = []

app = flask.Flask(__name__)

@app.route('/')
def index():
    reset()
    return flask.render_template('index.html')

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
        'ship_placements': ship_positions
    }
    return flask.render_template('game_board.html', **context)

@app.route('/play/redirect', methods=['GET'])
def play_redirect():
    global ship_positions, set_ships

    # Get ship placements from the query parameters and store them in the global variable
    ship_positions = json.loads(flask.request.args.get('ship_placements'))
    set_ships = False

    # Set ships on player and ai boards
    ai_board.set_ships(*testing_ship_positions)

    player_ship_positions = []
    for ship in ship_positions:
        positions = [tuple(pos) for pos in ship['positions']]
        player_ship_positions.append(positions)
    player_board.set_ships(*player_ship_positions)

    # Redirect to the /play route to start the game
    return flask.redirect('/play')

@app.route('/play/player-move', methods=['POST'])
def player_move():
    row, col = flask.request.json['row'], flask.request.json['col']

    # Register the player's move on the AI's board and return whether it was a hit or miss
    hit = ai_board.receive_attack((row, col))
    ai_board.turns += 1

    # Return game state as JSON to html
    response  = {
        'hit': hit,
        'ai_board': ai_board.grid.tolist(),
        'win': all(ship.sunk for ship in ai_board.ships)
    }

    print(ai_board.grid)
    return flask.jsonify(response)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()