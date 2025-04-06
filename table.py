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
    
    def get_plates(self, cakes, cake_offset): # Isto é para ir buscar à lista dos bolos
        num_needed = self.max_plates
        
        new_plates = cakes[cake_offset:cake_offset + num_needed]
        for plate in new_plates:
            self.add_plate(plate)
            
        new_offset = cake_offset + len(new_plates)
        return new_offset
    
    def get_plates_on_table(self):
        return [plate for plate in self.plates if plate is not None]
    
    def has_no_plates(self):
        return all(plate is None for plate in self.plates)

    def reset(self):
        self.plates = [None] * self.max_plates
    

    def clone(self):
        new_table = Table(self.padding, self.side_img_width, self.max_plates)
        new_table.plates = [plate.clone() if plate is not None else None for plate in self.plates]
        return new_table

    def __eq__(self, other):
        if not isinstance(other, Table):
            return False
        return (self.padding == other.padding and 
                self.table_side_img_width == other.table_side_img_width and
                self.plates == other.plates)

    def __str__(self):
        return f"Table(plates_on_table={self.plates})"
        