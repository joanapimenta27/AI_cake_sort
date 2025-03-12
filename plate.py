from slice import Slice

class Plate:
    def __init__(self, slices):
        self.max_slices = slices
        self.slices = [None] * slices
    
    def add_slices(self, cake_slice):
        for i in range(self.max_slices):
            if self.slices[i] is None:
                self.slices[i] = cake_slice
                return True
        return False

    def remove_slice(self, index):
        if 0 <= index < self.max_slices:
            removed = self.slices[index]
            self.slices[index] = None
            return removed
        return None
    
    def get_slice(self, index):
        if 0 <= index < self.max_slices:
            return self.slices[index]
        return None
    
    def is_full(self):
        return all(slice_ is not None for slice_ in self.slices)

    def is_empty(self):
        return all(slice_ is None for slice_ in self.slices)
    
    def number_of_slices(self):
        return sum(1 for slice_ in self.slices if slice_ is not None)