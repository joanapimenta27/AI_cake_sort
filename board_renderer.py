class BoardRenderer:
    def __init__(self, board, side_margin, top_margin, tile_image, cell_size):
        self.board = board
        self.side_margin = side_margin
        self.top_margin = top_margin
        self.tile_image = tile_image
        self.cell_size = cell_size
    
    def draw(self, screen):
        rows = self.board.rows
        cols = self.board.cols

        for row in range(rows):
            for col in range(cols):
                x = col * self.cell_size + self.side_margin
                y = row * self.cell_size + self.top_margin

                screen.blit(self.tile_image, (x, y))