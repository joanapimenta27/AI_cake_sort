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