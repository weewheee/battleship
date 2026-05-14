import numpy as np

def generate_next_move(board: np.ndarray, ship_sunk_state: list[bool]) -> tuple[int, int]:

    #* bool test_mode is used to determine whether to return heat map to display using decorator

    heat_map = np.array([[0] * 10 for _ in range(10)])

    # generate heat map based on all possible ship placements
    if 'X' not in board:
        for ship_size, sunk in zip([5, 4, 3, 3, 2], ship_sunk_state):

            # check if ship is already sunk
            if sunk:
                continue

            # place horizontally
            for i in range(10):
                for j in range(10 - ship_size + 1):

                    # skip if ship placement is not possible
                    if set(board[i, j:j + ship_size].ravel()) != {' '}:
                        continue

                    heat_map[i, j:j + ship_size] += 1

            # place vertically
            for i in range(10 - ship_size + 1):
                for j in range(10):

                    # skip if ship placement is not possible
                    if set(board[i:i + ship_size, j].ravel()) != {' '}:
                        continue
                    
                    heat_map[i:i + ship_size, j] += 1

    else:
        
        # target around hit locations
        for ship_size, sunk in zip([5, 4, 3, 3, 2], ship_sunk_state):

            # check if ship is already sunk
            if sunk:
                continue

            #* for each direction, check if ship can be placed. Prioritise a direction if there are multiple hits in a line in the same direction
            #*
            #* i.e.
            #* [ ,  ,  , ]
            #* [ , X, X, ]  -->    Horizontal search will be prioritised since there are multiple hits in a horizontal line
            #* [ ,  ,  , ]
            #*
            #* priority will be determined by number of hits for a possible ship placement by the following values:
            #*
            #*  hits | heat map value
            #* ------|----------------
            #*    1  |      1
            #*    2  |     10
            #*    3  |     20
            #*    4  |     30

            PRIORITY_VALUES = [0, 1, 10, 20, 30]
                      
            # check all possible horizontal placements if it coincides with hit locations
            for i in range(10):
                for j in range(10 - ship_size + 1):

                    # skip if ship placement is not possible or does not coincide with hit locations
                    if set(board[i, j:j + ship_size].ravel()) != {' ', 'X'}:
                        continue

                    heat_map[i, j:j + ship_size][board[i, j:j + ship_size] == ' '] += PRIORITY_VALUES[np.count_nonzero(board[i, j:j + ship_size] == 'X')]

            # check all possible vertical placements if it coincides with hit locations
            for i in range(10 - ship_size + 1):
                for j in range(10):

                    # skip if ship placement is not possible or does not coincide with hit locations
                    if set(board[i:i + ship_size, j].ravel()) != {' ', 'X'}:
                        continue

                    heat_map[i:i + ship_size, j][board[i:i + ship_size, j] == ' '] += PRIORITY_VALUES[np.count_nonzero(board[i:i + ship_size, j] == 'X')]
    
    return tuple([int(i) for i in np.unravel_index(heat_map.argmax(), heat_map.shape)])