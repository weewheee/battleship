import numpy as np
import random

class Ship:
    def __init__(self, size: int) -> None:
        self.size: int = size
        self.position_unhit: set[tuple[int, int]] = set()
        self.position_hit: set[tuple[int, int]] = set()

        self.hits: int = 0
        self.sunk: bool = False

    def place(self, positions: list[tuple[int, int]]) -> None:
        self.position_unhit = set(positions)

    def register_hit(self, position: tuple[int, int]) -> bool:
        # return True if hit, False if miss
        
        if position not in self.position_unhit:
            return False

        self.position_unhit.remove(position)
        self.position_hit.add(position)
        self.hits += 1
        if self.hits == self.size:
            self.sunk = True
        return True    

class Board:
    def __init__(self) -> None:
        self.grid: np.ndarray = np.array([[' '] * 10 for _ in range(10)])
        self.ships: list[Ship] = [Ship(size) for size in [5, 4, 3, 3, 2]]

        self.turns: int = 0

    def set_ships(self, *positions: list[list[tuple[int, int]]]) -> None:
        # If positions are provided, set ships to the positions
        if positions != ():
            for ship, pos in zip(self.ships, positions):
                ship.place(pos)
            return 
        
        # randomise ship placement if no positions provided
        all_positions = set()

        for ship in self.ships:
            while True:

                orientation = random.choice(['horizontal', 'vertical'])
                if orientation == 'horizontal':
                    row = random.randint(0, 9)
                    col = random.randint(0, 10 - ship.size)
                    ship.position_unhit = {(row, col + i) for i in range(ship.size)}
                else:
                    row = random.randint(0, 10 - ship.size)
                    col = random.randint(0, 9)
                    ship.position_unhit = {(row + i, col) for i in range(ship.size)}
                
                # Check for overlap
                if not all_positions.intersection(ship.position_unhit):
                    all_positions.update(ship.position_unhit)
                    break

    def receive_attack(self, position: tuple[int, int]) -> bool:
        for ship in self.ships: 
            if ship.register_hit(position):
                self.grid[position[0], position[1]] = 'X'  # Mark hit

                # Check if the ship is sunk
                if ship.sunk:
                    for i, j in ship.position_hit:
                        self.grid[i, j] = 'S'  # Mark sunk
                return True
            
        self.grid[position[0], position[1]] = 'O'  # Mark miss
        return