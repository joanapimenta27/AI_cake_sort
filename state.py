import copy

class State:
    def __init__(self, board, table, cake_offset, scoreboard):
        self.board = board.clone()
        self.table = table.clone()
        self.cake_offset = cake_offset
        self.scoreboard = scoreboard.clone()

    def copy(self):
        return State(self.board, self.table, self.cake_offset, self.scoreboard)
    
    def __eq__(self, other):
        return (self.board == other.board and 
                self.table == other.table and 
                self.cake_offset == other.cake_offset and
                self.scoreboard == other.score)
    
    def __hash__(self):
        return hash((str(self.board), str(self.table), self.cake_offset, str(self.scoreboard)))
    
    def __str__(self, cakes=False):
        if cakes:
            return f"Score: {self.scoreboard.score}\nBoard: {self.board}\nTable: {self.table}\nCakes: {self.cake_offset}"
        else:
            return f"Score: {self.scoreboard.score}\nBoard: {self.board}\nTable: {self.table}"
