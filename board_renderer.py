import pygame

class BoardRenderer:
    def __init__(self, board, side_margin, top_margin, tile_image, hover_tile_img, cell_size):
        self.board = board
        self.side_margin = side_margin
        self.top_margin = top_margin
        self.tile_image = tile_image
        self.hover_tile_img = hover_tile_img
        self.cell_size = cell_size
    
    def draw(self, screen, selected_plate=None):
        mouse_pos = pygame.mouse.get_pos()
        rows = self.board.rows
        cols = self.board.cols

        for row in range(rows):
            for col in range(cols):
                x = col * self.cell_size + self.side_margin
                y = row * self.cell_size + self.top_margin
                tile_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                if selected_plate is not None and tile_rect.collidepoint(mouse_pos) and self.board.is_valid_tile(row, col):
                    screen.blit(self.hover_tile_img, (x, y))
                else:
                    screen.blit(self.tile_image, (x, y))