import pygame

from board import Board
from plate import Plate
from slice import Slice
from plate_renderer import PlateRenderer
from slice_renderer import SliceRenderer
from board_renderer import BoardRenderer

def main():
    pygame.init()

    screen_width = 900
    screen_height = 900


    #========================= PREPARE CELL SIZE ==========================#
    rows, cols = 4, 4  # Numero de linhas e colunas do tabuleiro
    board_min_sides_margin = 50  # Margem lateral minima do tabuleiro
    board_min_top_margin = 25  # Margem superior mínima do tabuleiro
    table_margin_top = 100  # Espaço minimo entre a mesa e o tabuleiro
    table_padding = 25  # Padding da mesa
    #--> Calcular cell_size baseado nas margens e nas linhas e colunas
    cell_size = int(min((screen_width - board_min_sides_margin) / cols, (screen_height - table_margin_top - table_padding - board_min_top_margin) / (rows+1)))
    #_________________________ PREPARE CELL SIZE __________________________#


    #=========================== PREPARE CAKES ============================#
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cake Sort")
    chocolate_img = pygame.image.load("assets/chocolate_cake.png")
    chocolate_img = pygame.transform.scale(chocolate_img, (cell_size, cell_size))
    strawberry_img = pygame.image.load("assets/strawberry_cake.png")
    strawberry_img = pygame.transform.scale(strawberry_img, (cell_size, cell_size))
    cake_data = [chocolate_img, strawberry_img]
    slice_count = 6
    #___________________________ PREPARE CAKES ____________________________#


    #=========================== RENDER BOARD =============================#
    board_side_margin = (screen_width - cell_size*cols)/2
    board_top_margin = (screen_height - cell_size*rows - table_margin_top - table_padding)/2
    #--> Render do Tabuleiro
    board = Board(rows, cols)
    tile_image = pygame.image.load("assets/tile.png")
    tile_image = pygame.transform.scale(tile_image, (cell_size, cell_size))
    board_renderer = BoardRenderer(board, board_side_margin, board_top_margin, tile_image, cell_size)
    #--> Render dos slices
    slice_renderer = SliceRenderer(cake_data, slice_count)
    #--> Render dos plates
    plate_img = pygame.transform.scale(pygame.image.load("assets/plate.png"), (cell_size, cell_size))
    plate_renderer = PlateRenderer(board, board_side_margin, board_top_margin, plate_img, cell_size, slice_renderer)
    #___________________________ RENDER BOARD _____________________________#

    plate = Plate(slice_count)
    plate.add_slices(Slice(0))
    plate.add_slices(Slice(1))


    board.place_item(2, 2, plate)

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((200, 200, 250))

        board_renderer.draw(screen)
        plate_renderer.draw(screen)

        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()