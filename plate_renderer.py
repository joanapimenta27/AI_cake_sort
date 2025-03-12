import math

from plate import Plate

class PlateRenderer:
    def __init__(self, board, side_margin, top_margin, plate_image, cell_size, slice_renderer):
        self.board = board
        self.side_margin = side_margin
        self.top_margin = top_margin
        self.plate_image = plate_image
        self.cell_size = cell_size
        self.slice_renderer = slice_renderer

    
    def draw(self, screen):
        rows = self.board.rows
        cols = self.board.cols

        for row in range(rows):
            for col in range(cols):
                item = self.board.get_item(row, col)
                if isinstance(item, Plate):
                    x = col * self.cell_size + self.side_margin
                    y = row * self.cell_size + self.top_margin

                    screen.blit(self.plate_image, (x, y))

                    cx = x + self.plate_image.get_width() // 2
                    cy = y + self.plate_image.get_height() // 2

                    for i, slice in enumerate(item.slices):
                        if slice is not None:
                            self.slice_renderer.draw_slice(screen, slice.cake_index(), i, cx, cy)

                
