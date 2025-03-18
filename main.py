import pygame

from input_handler import *
from menu import Menu
from settings import SettingsMenu
from scoreboard import Scoreboard
from board import Board
from plate import Plate
from slice import Slice
from table import Table
from plate_renderer import PlateRenderer
from slice_renderer import SliceRenderer
from board_renderer import BoardRenderer
from table_renderer import TableRenderer

def main():
    pygame.init()

    screen_width = 900
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cake Sort")

    menu=Menu(screen)
    in_menu= True

    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            action = menu.handle_event(event)

            if action == "start":
                in_menu = False
            elif action == "settings":
                settings_menu = SettingsMenu(screen)
                running_settings = True
                while running_settings:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        action = settings_menu.handle_event(event)
                        if action == "back":
                            running_settings = False

                    settings_menu.draw()
                    pygame.display.flip()
        menu.draw()
        pygame.display.flip()

    #========================= PREPARE CELL SIZE ==========================#
    rows, cols = 4, 4  # Numero de linhas e colunas do tabuleiro
    board_min_sides_margin = 50  # Margem lateral minima do tabuleiro
    board_min_top_margin = 100  # Margem superior mínima do tabuleiro
    table_margin_top = 100  # Espaço minimo entre a mesa e o tabuleiro
    table_padding = 25  # Padding da mesa
    #--> Calcular cell_size baseado nas margens e nas linhas e colunas
    cell_size = int(min((screen_width - board_min_sides_margin) / cols, (screen_height - table_margin_top - table_padding*2 - board_min_top_margin) / (rows+1)))
    #_________________________ PREPARE CELL SIZE __________________________#


    #========================= PREPARE ANIMATIONS =========================#
    circle_highlight_img = pygame.image.load("assets/circle_highlight.png")
    circle_highlight_img = pygame.transform.scale(circle_highlight_img, (cell_size, cell_size))
    #_________________________ PREPARE ANIMATIONS _________________________#


    #=========================== PREPARE CAKES ============================#
    chocolate_img = pygame.image.load("assets/chocolate_cake.png")
    chocolate_img = pygame.transform.scale(chocolate_img, (cell_size, cell_size))
    pistaccio_img = pygame.image.load("assets/pistaccio_cake.png")
    pistaccio_img = pygame.transform.scale(pistaccio_img, (cell_size, cell_size))
    strawberry_img = pygame.image.load("assets/strawberry_cake.png")
    strawberry_img = pygame.transform.scale(strawberry_img, (cell_size, cell_size))
    cake_data = [chocolate_img, strawberry_img, pistaccio_img]
    slice_count = 6
    Plate.cake_data = cake_data
    Plate.max_slices = slice_count
    #___________________________ PREPARE CAKES ____________________________#


    #=========================== RENDER BOARD =============================#
    board_side_margin = (screen_width - cell_size*cols)/2
    board_top_margin = (screen_height - cell_size*(rows+1) - table_margin_top - table_padding*2)
    #--> Render do Tabuleiro
    board = Board(rows, cols)
    tile_image = pygame.image.load("assets/tile.png")
    tile_image = pygame.transform.scale(tile_image, (cell_size, cell_size))
    hover_tile_img = pygame.image.load("assets/hover_tile.png")
    hover_tile_img = pygame.transform.scale(hover_tile_img, (cell_size, cell_size))
    board_renderer = BoardRenderer(board, board_side_margin, board_top_margin, tile_image, hover_tile_img, cell_size)
    #--> Render da Mesa
    table_side_img_width = 100
    table = Table(table_padding, table_side_img_width, 3)
    table.generate_random_plates()
    table_side_img = pygame.image.load("assets/table_side.png")
    table_side_img = pygame.transform.scale(table_side_img, (table_side_img_width, cell_size + table_padding*2))
    table_img = pygame.image.load("assets/table.png")
    table_img = pygame.transform.scale(table_img, (screen_width-table_side_img_width*2, cell_size + table_padding*2))
    table_renderer = TableRenderer(table, table_padding, table_img, table_side_img, cell_size)
    #--> Render dos slices
    slice_renderer = SliceRenderer(cake_data, slice_count)
    #--> Render dos plates
    plate_img = pygame.transform.scale(pygame.image.load("assets/plate.png"), (cell_size, cell_size))
    plate_renderer = PlateRenderer(board, table, board_side_margin, board_top_margin, plate_img, circle_highlight_img, cell_size, slice_renderer)
    #___________________________ RENDER BOARD _____________________________#

    #=========================== PREPARE SCOREBOARD =============================#
    scoreboard = Scoreboard(screen)
    #___________________________ PREPARE SCOREBOARD _____________________________#

    selected_plate = None
    plate_is_selected = False

    #============================= MAIN LOOP ==============================#
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not plate_is_selected:
                    pos = pygame.mouse.get_pos()
                    selected_plate = handle_plate_selection(pos, selected_plate, board, table, board_side_margin, board_top_margin, cell_size)
        
        if table.has_no_plates():
            table.generate_random_plates()
        
        screen.fill((200, 200, 250))

        board_renderer.draw(screen, selected_plate)
        table_renderer.draw(screen)
        plate_renderer.draw(screen, selected_plate)

        board.clean_board(scoreboard)

        scoreboard.draw()
        
        pygame.display.flip()
    #____________________________ MAIN LOOP ______________________________#
    
    pygame.quit()


if __name__ == "__main__":
    main()