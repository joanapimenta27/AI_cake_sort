import copy

class State:
    def __init__(self, board, table, cakes, scoreboard):
        self.board = board.clone()
        self.table = table.clone()
        self.cakes = copy.deepcopy(cakes)
        self.scoreboard = scoreboard.clone()

    def copy(self):
        return State(self.board, self.table, copy.deepcopy(self.cakes), self.scoreboard)
    
    def __eq__(self, other):
        return (self.board == other.board and 
                self.table == other.table and 
                self.cakes == other.cakes and
                self.scoreboard == other.score)
    
    def __hash__(self):
        return hash((str(self.board), str(self.table), tuple(self.cakes), str(self.scoreboard)))
    
    def __str__(self, cakes=True):
        if cakes:
            return f"Score: {self.scoreboard.score}\nBoard: {self.board}\nTable: {self.table}\nCakes: {self.cakes}"
        else:
            return f"Score: {self.scoreboard.score}\nBoard: {self.board}\nTable: {self.table}"
