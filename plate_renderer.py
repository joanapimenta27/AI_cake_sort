import math
import pygame
from plate import Plate
from animation import pulsing_alpha_animation

class PlateRenderer:
    def __init__(self, board, table, side_margin, top_margin, plate_image, highlight_img, cell_size, slice_renderer):
        self.board = board
        self.table = table
        self.side_margin = side_margin
        self.top_margin = top_margin
        self.plate_image = plate_image
        self.highlight_img = highlight_img
        self.cell_size = cell_size
        self.slice_renderer = slice_renderer
        self.spacing = 0

    
    def draw(self, screen, selected_plate=None):
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

        # RENDER IN TABLE
        table_height = self.cell_size + self.table.padding*2
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        side_width = self.table.side_img_width
        table_width = screen_width - 2 * side_width
        plates = self.table.plates
        max_plates = self.table.max_plates
        num_plates = len(self.table.plates)

        if num_plates > 0:
            self.spacing = (table_width - self.cell_size*max_plates) // (max_plates + 1)
            for i, plate in enumerate(plates):
                if plate is not None:
                    cx = side_width + self.spacing + i * (self.cell_size + self.spacing)
                    cy = screen_height - table_height + self.table.padding
                    screen.blit(self.plate_image, (cx, cy))

                    for j, slice in enumerate(plate.slices):
                        if slice is not None:
                            self.slice_renderer.draw_slice(screen, slice.cake_index(), j, cx + self.cell_size // 2, cy + self.cell_size // 2)
                
                    if plate == selected_plate:
                        alpha = pulsing_alpha_animation()
                        pulsing_highlight = self.highlight_img.copy()
                        pulsing_highlight.set_alpha(alpha)
                        screen.blit(pulsing_highlight, (cx, cy)) 

                
