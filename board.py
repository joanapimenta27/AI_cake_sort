import pygame

from plate import Plate

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
    
    def is_inside_board(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def place_item(self, row, col, item):
        if not self.is_inside_board(row, col):
            raise ValueError(f"Invalid board position: ({row}, {col})")
        elif self.is_valid_tile(row, col):
            self.grid[row][col] = item
    
    def remove_item(self, row, col):
        if not self.is_inside_board(row, col):
            raise ValueError(f"Invalid board position: ({row}, {col})")
        removed = self.grid[row][col]
        self.grid[row][col] = None
        return removed
    
    def get_item(self, row, col):
        if not self.is_inside_board(row, col):
            raise ValueError(f"Invalid board position: ({row}, {col})")
        return self.grid[row][col]

    def is_valid_tile(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        return self.get_item(row, col) is None
    
    def get_adjacent_plates(self, row, col):
        adjacent = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r, c = row + dr, col + dc
            if self.is_inside_board(r, c):
                item = self.get_item(r, c)
                if isinstance(item, Plate):
                    adjacent.append(item)
        return adjacent
    
    def clean_board(self,score):
        positions_to_remove = []
        for row in range(self.rows):
            for col in range(self.cols):
                item = self.get_item(row, col)
                if item is not None:
                    if isinstance(item, Plate) and (item.is_empty() or item.is_fully_uniform()):
                        positions_to_remove.append((row, col,item))

        for row,col, plate in positions_to_remove:
            if  plate.is_empty():
                score.update_score(10)  # Award 10 points for an empty plate.
            elif plate.is_fully_uniform():
                score.update_score(20)  # Award 20 points for a complete cake.           
            pygame.display.flip()
            pygame.time.delay(600//len(positions_to_remove))
            self.remove_item(*(row,col))
            pygame.display.flip()

        