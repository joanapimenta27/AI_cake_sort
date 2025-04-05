class Slice:
    def __init__(self, cake_index):
        self.flavor = cake_index
    
    def cake_index(self):
        return self.flavor

    def clone(self):
        return Slice(self.flavor)
    
    def __eq__(self, other):
        if not isinstance(other, Slice):
            return False
        return self.flavor == other.flavor
    