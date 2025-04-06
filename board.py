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
    
    def clean_board(self, score, delay=True):
        positions_to_remove = []
        for row in range(self.rows):
            for col in range(self.cols):
                item = self.get_item(row, col)
                if item is not None:
                    if isinstance(item, Plate) and (item.is_empty() or item.is_fully_uniform()):
                        positions_to_remove.append((row, col,item))

        for row,col, plate in positions_to_remove:
            if  plate.is_empty():
                score.update_score(10)
            elif plate.is_fully_uniform():
                score.update_score(20)
            pygame.display.flip()
            if delay:
                pygame.time.delay(600//len(positions_to_remove))
            self.remove_item(*(row,col))
            pygame.display.flip()
    
    def reset(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = None

    

    def clone(self):
        new_board = Board(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] is not None:
                    new_board.grid[i][j] = self.grid[i][j].clone()
                else:
                    new_board.grid[i][j] = None
        return new_board

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        return self.rows == other.rows and self.cols == other.cols and self.grid == other.grid

    def __str__(self):
        grid_str = "\n".join(str(row) for row in self.grid)
        return f"Board({self.rows}x{self.cols}):\n{grid_str}"
    
    def get_cakes_from_board(self):
        all_slices = []

        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.grid[x][y]
                if isinstance(cell, Plate):
                    all_slices.append(cell)

        return all_slices



        