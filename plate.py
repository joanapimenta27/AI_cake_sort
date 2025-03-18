import random
from slice import Slice

class Plate:

    max_slices = 6
    cake_data = []

    def __init__(self):
        self.slices = [None] * self.max_slices
    
    def add_slice(self, cake_slice):
        for i in range(self.max_slices):
            if self.slices[i] is None:
                self.slices[i] = cake_slice
                non_empty = [s for s in self.slices if s is not None]
                non_empty.sort(key=lambda s: s.cake_index())
                self.slices = non_empty + [None] * (self.max_slices - len(non_empty))
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
    
    def get_number_of_distinct_flavors(self):
        return len(set(slice_.cake_index() for slice_ in self.slices if slice_ is not None))
    
    def get_dominant_flavor(self):
        counts = {}
        for slice_ in self.slices:
            if slice_ is not None:
                flavor = slice_.cake_index()
                counts[flavor] = counts.get(flavor, 0) + 1
        if counts:
            return max(counts, key=counts.get), max(counts.values())
        return None
    
    def get_flavor_count(self, flavor):
        return sum(1 for slice_ in self.slices if slice_ is not None and slice_.cake_index() == flavor)
    
    def is_fully_uniform(self):
        return self.get_number_of_distinct_flavors() == 1 and self.is_full()
    
    def is_full(self):
        return all(slice_ is not None for slice_ in self.slices)

    def is_empty(self):
        return all(slice_ is None for slice_ in self.slices)
    
    def number_of_slices(self):
        return sum(1 for slice_ in self.slices if slice_ is not None)
    
    def number_of_flavors_available(self):
        return len(self.cake_data)
    
    def generate_random_plate(self):
        number_of_slices = random.randint(1, self.max_slices-1)
        number_of_flavors = self.number_of_flavors_available()
        for i in range(number_of_slices):
            flavor = random.randint(0, number_of_flavors-1)
            slice = Slice(flavor)
            self.add_slice(slice)
