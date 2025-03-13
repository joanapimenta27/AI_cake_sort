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