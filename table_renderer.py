import pygame

class TableRenderer:
    def __init__(self, table, padding, img, side_img, cell_size):
        self.table = table
        self.padding = padding
        self.img = img
        self.side_img = side_img
        self.cell_size = cell_size
    
    def draw(self, screen):
        table_height = self.cell_size + self.padding*2
        screen_height = screen.get_height()

        side_width = int(self.side_img.get_width())
        side_img_mirrored = pygame.transform.flip(self.side_img, True, False)

        screen.blit(self.side_img, (0, screen_height - table_height))
        screen.blit(side_img_mirrored, (screen.get_width() - side_width, screen_height - table_height))
        screen.blit(self.img, (side_width, screen_height - table_height))


    