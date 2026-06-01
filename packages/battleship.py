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
        """Registers a hit on the ship at the given position. 
        Returns a Boolean indicating whether the ship was hit."""

        # Return False if hit location is not part of ship or has already been hit
        if position not in self.position_unhit:
            return False

        # If hit location is part of ship and has not already been hit, register hit and return True
        self.position_unhit.remove(position)
        self.position_hit.add(position)
        self.hits += 1
        self.sunk = self.hits == self.size  # Ship is sunk if number of hits equals size of ship
        return True    

class Board:
    def __init__(self) -> None:
        self.grid: np.ndarray = np.array([[' '] * 10 for _ in range(10)])
        self.ships: list[Ship] = [Ship(size) for size in [5, 4, 3, 3, 2]]

        self.hit_count: int = 0
        self.miss_count: int = 0

    def set_ships(self, *positions: list[list[tuple[int, int]]]) -> None:
        """Sets ship positions on the board. 
        If no positions are provided, randomises ship placement."""
        
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

    def receive_attack(self, position: tuple[int, int]) -> tuple[bool, list[tuple[int, int]]]: 
        """Registers an attack on the board at the given position. 
        Returns a Boolean indicating a hit, and a list of sink positions if a ship is sunk."""
        
        for ship in self.ships: 
            # Skip ship if it is not hit
            if not ship.register_hit(position):
                continue

            # If ship is hit
            self.hit_count += 1
            
            self.grid[position[0], position[1]] = 'X'  # Mark hit

            # End process if ship is not sunk
            if not ship.sunk:
                return True, []

            # Else if ship has been sunk, mark sunk
            for i, j in ship.position_hit:
                self.grid[i, j] = 'S'  # Mark sunk

            # return True and the positions of the sunk ship
            return True, list(ship.position_hit)

        # If no ships were hit by attack
        self.miss_count += 1;    
        self.grid[position[0], position[1]] = 'O'  # Mark miss
        return False, []  # Return False for miss