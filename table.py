import random
from plate import Plate
from slice import Slice


class Table:
    DEFAULT_MAX_PLATES = 3

    def __init__(self, padding, side_img_width, max_plates=DEFAULT_MAX_PLATES):
        self.padding = padding
        self.side_img_width = side_img_width
        self.max_plates = max_plates
        self.plates = [None] * max_plates
    
    def add_plate(self, plate):
        for i in range(self.max_plates):
            if self.plates[i] is None:
                self.plates[i] = plate
                return True
        return False
    
    def remove_plate(self, index):
        if 0 <= index < self.max_plates:
            removed = self.plates[index]
            self.plates[index] = None
            return removed
        ValueError(f"Invalid plate index: {index}")
        return None
    
    def generate_random_plates(self):
        for i in range(self.max_plates):
            plate = Plate()
            plate.generate_random_plate()
            self.add_plate(plate)
    
    def has_no_plates(self):
        return all(plate is None for plate in self.plates)
        