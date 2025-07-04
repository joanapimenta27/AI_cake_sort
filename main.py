import pygame
import csv
import time
import os

from input_handler import *
from utils import *
from algorithm import *
from menu import Menu
from scoreboard import Scoreboard
from board import Board
from plate import Plate
from table import Table
from state import State
from plate_renderer import PlateRenderer
from slice_renderer import SliceRenderer
from board_renderer import BoardRenderer
from table_renderer import TableRenderer





def main():

    pygame.init()

    game_state = "Menu"

    screen_width = 900
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cake Sort")

    board = None
    table = None
    board_renderer = None
    table_renderer = None
    plate_renderer = None
    cakes = None
    scoreboard = None
    selected_plate = None
    pause_button_rect = None
    hint_button_rect = None
    cake_offset = 0
    plate_is_selected = False
    board_side_margin = None
    board_top_margin = None
    cell_size = None
    rows, cols = 3, 3
    slice_count = 6
    number_of_cakes = 20
    plates_on_table = 3
    helper_algorithm = "BFS"
    hint_move = None
    table_x = None
    table_y = None
    plate_padding = 10





    def initialize_game():
        nonlocal board_renderer, table_renderer, plate_renderer, cakes, scoreboard, board, table, selected_plate, pause_button_rect, hint_button_rect, cake_offset, plate_is_selected
        nonlocal board_side_margin, board_top_margin, cell_size, table_x, table_y, plate_padding, hint_move

        hint_move = None
        #========================= PREPARE CELL SIZE ==========================#
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
        pie_img = pygame.image.load("assets/pie_cake.png")
        pie_img = pygame.transform.scale(pie_img, (cell_size, cell_size))
        cheese_img = pygame.image.load("assets/cheese_cake.png")
        cheese_img = pygame.transform.scale(cheese_img, (cell_size, cell_size))
        cake_data = [chocolate_img, strawberry_img, pistaccio_img, pie_img, cheese_img]
        Plate.cake_data = cake_data
        Plate.max_slices = slice_count
        #--> Gerar os bolos
        seed = 69
        cakes = generate_cakes(cake_data, slice_count, number_of_cakes, seed)
        cake_offset = 0
        #print(cakes)
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
        table = Table(table_padding, table_side_img_width, plates_on_table)
        table_x = table_side_img_width
        table_y = screen_height - (cell_size+table_padding*2) + table_padding
        cake_offset = table.get_plates(cakes, cake_offset)
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
        plate_padding = plate_renderer.spacing
        #___________________________ RENDER BOARD _____________________________#

        #=========================== PREPARE SCOREBOARD =============================#
        scoreboard = Scoreboard(screen)
        pause_button_rect = pygame.Rect(screen_width - 20 - 60, 20, 60, 60)
        hint_button_rect = pygame.Rect(20, 20, 60, 60)
        #___________________________ PREPARE SCOREBOARD _____________________________#

        selected_plate = None
        plate_is_selected = False

    #============================ PREPARE MENU =============================#
    initialize_game()
    algorithm_depth = 2
    algorithm_iterations = 500
    visualize = False
    menu = Menu(screen)
    ai_menu = Menu(screen, "AIMenu")
    bfs_menu = Menu(screen, "BFSMenu")
    dfs_menu = Menu(screen, "DFSMenu")
    monte_carlo_menu = Menu(screen, "MonteCarloMenu")
    greedy_menu = Menu(screen, "GreedyMenu")
    a_menu = Menu(screen, "A*Menu")
    game_over_menu = Menu(screen, "GameOver", scoreboard.score)
    settings_menu = Menu(screen, "SettingsMenu")
    #__________________________ PREPARE MENU _____________________________#

    #============================= MAIN LOOP ==============================#
    running = True
    while running:
        match game_state:

            case "Menu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        #+sys.exit()
                    action = menu.handle_event(event)
                    if action == "start":
                        game_state = "Playing"
                        initialize_game()
                    elif action == "aiMenu":
                        game_state = "AIMenu"
                    elif action == "settings":
                        game_state = "SettingsMenu"
                menu.draw()
                pygame.display.flip()
            

            case "SettingsMenu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        #+sys.exit()
                    action = settings_menu.handle_event(event)
                    adjust = settings_menu.handle_int_button_event(event)
                    if adjust:
                        rows, cols, number_of_cakes, slice_count, plates_on_table, helper_algorithm = adjust
                    if action == "back":
                        game_state = "Menu"
                        initialize_game()
                    
                settings_menu.draw()
                pygame.display.flip()

            case "AIMenu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        #+sys.exit()
                    action = ai_menu.handle_event(event)
                    if action == "BFS":
                        game_state = "BFSMenu"
                    elif action == "DFS":
                        game_state = "DFSMenu"
                    elif action == "Greedy":
                        game_state = "GreedyMenu"
                    elif action == "AStar":
                        game_state="A*Menu"
                    elif action == "Monte Carlo":
                        game_state = "MonteCarloMenu"
                    elif action == "back":
                        game_state = "Menu"
                ai_menu.draw()
                pygame.display.flip()
            
            case "BFSMenu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        #+sys.exit()
                    action = bfs_menu.handle_event(event)
                    adjust = bfs_menu.handle_int_button_event(event)
                    if action == "start_1":
                        visualize = False
                        game_state = "BFSPlaying"
                        algorithm_depth = adjust
                    elif action == "start_2":
                        visualize = True
                        game_state = "BFSPlaying"
                        algorithm_depth = adjust
                    elif action == "back":
                        game_state = "AIMenu"
                bfs_menu.draw()
                pygame.display.flip()

            case "DFSMenu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        #+sys.exit()
                    action = dfs_menu.handle_event(event)
                    adjust = dfs_menu.handle_int_button_event(event)
                    if action == "start_1":
                        visualize = False
                        game_state = "DFSPlaying"
                        algorithm_depth = adjust
                    elif action == "start_2":
                        visualize = True
                        game_state = "DFSPlaying"
                        algorithm_depth = adjust
                    elif action == "back":
                        game_state = "AIMenu"
                dfs_menu.draw()
                pygame.display.flip()
            

            case "DFSPlaying":
                screen.fill((200, 200, 250))
                board_renderer.draw(screen)
                table_renderer.draw(screen)
                plate_renderer.draw(screen)
                scoreboard.draw()
                pygame.display.flip()
                current_state = State(board, table, cake_offset, scoreboard)

                start_time = time.perf_counter()
                best_moves, nodes_visited = dfs_solver(current_state, algorithm_depth, cakes)
                end_time = time.perf_counter()

                time_taken = end_time - start_time

                csv_file_path = "results/dfs_metrics.csv"
                file_exists = os.path.isfile(csv_file_path)

                if not visualize:
                    with open("results/dfs_metrics.csv", "a", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        if not file_exists:
                            writer.writerow(["Time Taken", "Nodes Visited", "Algorithm Depth", "Best Moves Count", "Cakes Count", "Score"])
                        writer.writerow([time_taken, nodes_visited, algorithm_depth, len(best_moves), len(cakes), scoreboard.score])
                
                if (len(best_moves) == len(cakes) - cake_offset + len(current_state.table.get_plates_on_table())) and len(best_moves) > 0:
                    for move in best_moves:
                        new_state = apply_move(current_state, move, cakes)
                        
                        board = new_state.board
                        table = new_state.table
                        cake_offset = new_state.cake_offset
                        scoreboard = Scoreboard(screen)
                        scoreboard.score = new_state.scoreboard.score
                        
                        board_renderer.board = board
                        table_renderer.table = table
                        plate_renderer.board = board
                        plate_renderer.table = table
                        
                        screen.fill((200, 200, 250))
                        board_renderer.draw(screen)
                        table_renderer.draw(screen)
                        plate_renderer.draw(screen)
                        scoreboard.draw()
                        pygame.display.flip()
                        
                        if visualize:
                            pygame.time.delay(2000)
                        
                        current_state = new_state

                elif best_moves:
                    next_move = best_moves[0]
                    new_state = apply_move(current_state, next_move, cakes)
                    
                    board = new_state.board
                    table = new_state.table
                    cake_offset = new_state.cake_offset
                    scoreboard = Scoreboard(screen)
                    scoreboard.score = new_state.scoreboard.score

                    board_renderer.board = board
                    table_renderer.table = table
                    plate_renderer.board = board
                    plate_renderer.table = table


                    if visualize:
                        pygame.time.delay(2000)

                else:
                    print("No valid move found. Ending DFSPlaying state.")
                    game_state = "GameOver"
                
            
            case "BFSPlaying":
                screen.fill((200, 200, 250))
                board_renderer.draw(screen)
                table_renderer.draw(screen)
                plate_renderer.draw(screen)
                scoreboard.draw()
                pygame.display.flip()

                current_state = State(board, table, cake_offset, scoreboard)

                start_time = time.perf_counter()
                best_moves, nodes_visited = bfs_solver(current_state, algorithm_depth, cakes)
                end_time = time.perf_counter()

                time_taken = end_time - start_time

                csv_file_path = "results/bfs_metrics.csv"
                file_exists = os.path.isfile(csv_file_path)

                if not visualize:
                    with open("results/bfs_metrics.csv", "a", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        if not file_exists:
                            writer.writerow(["Time Taken", "Nodes Visited", "Algorithm Depth", "Best Moves Count", "Cakes Count", "Score"])
                        writer.writerow([time_taken, nodes_visited, algorithm_depth, len(best_moves), len(cakes), scoreboard.score])
                    
                if (len(best_moves) == len(cakes) - current_state.cake_offset + len(current_state.table.get_plates_on_table())) and len(best_moves) > 0:
                    for move in best_moves:
                        new_state = apply_move(current_state, move, cakes)
                        
                        board = new_state.board
                        table = new_state.table
                        cake_offset = new_state.cake_offset
                        scoreboard = Scoreboard(screen)
                        scoreboard.score = new_state.scoreboard.score
                        
                        board_renderer.board = board
                        table_renderer.table = table
                        plate_renderer.board = board
                        plate_renderer.table = table
                        
                        screen.fill((200, 200, 250))
                        board_renderer.draw(screen)
                        table_renderer.draw(screen)
                        plate_renderer.draw(screen)
                        scoreboard.draw()
                        pygame.display.flip()
                        
                        if visualize:
                            pygame.time.delay(2000)
                        
                        current_state = new_state
                        

                elif best_moves:
                    next_move = best_moves[0]
                    new_state = apply_move(current_state, next_move, cakes)
                
                    
                    board = new_state.board
                    table = new_state.table
                    cake_offset = new_state.cake_offset
                    scoreboard = Scoreboard(screen)
                    scoreboard.score = new_state.scoreboard.score

                    board_renderer.board = board
                    table_renderer.table = table
                    plate_renderer.board = board
                    plate_renderer.table = table


                    if visualize:
                        pygame.time.delay(2000)

                else:
                    print("No valid move found. Ending BFSPlaying state.")
                    game_state = "GameOver"

            

            case "MonteCarloMenu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        #+sys.exit()
                    action = monte_carlo_menu.handle_event(event)
                    adjust = monte_carlo_menu.handle_int_button_event(event)
                    if action == "start_1":
                        visualize = False
                        game_state = "MonteCarloPlaying"
                        algorithm_iterations, algorithm_depth = adjust
                    elif action == "start_2":
                        visualize = True
                        game_state = "MonteCarloPlaying"
                        algorithm_iterations, algorithm_depth = adjust
                    elif action == "back":
                        game_state = "AIMenu"
                monte_carlo_menu.draw()
                pygame.display.flip()
            

            case "MonteCarloPlaying":
                screen.fill((200, 200, 250))
                board_renderer.draw(screen)
                table_renderer.draw(screen)
                plate_renderer.draw(screen)
                scoreboard.draw()
                pygame.display.flip()

                current_state = State(board, table, cake_offset, scoreboard)
                subset_cakes = cakes[cake_offset - current_state.table.max_plates: cake_offset - current_state.table.max_plates + algorithm_depth ]
                
                start_time = time.perf_counter()
                best_moves, nodes_visited = monte_carlo_solver(current_state, algorithm_iterations, algorithm_depth, subset_cakes)
                end_time = time.perf_counter()

                time_taken = end_time - start_time

                csv_file_path = "results/mc_metrics.csv"
                file_exists = os.path.isfile(csv_file_path)

                if not visualize:
                    with open("results/mc_metrics.csv", "a", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        if not file_exists:
                            writer.writerow(["Time Taken", "Nodes Visited", "Algorithm Depth", "Algorithm Iterations", "Best Moves Count", "Cakes Count", "Score"])
                        writer.writerow([time_taken, nodes_visited, algorithm_depth, algorithm_iterations, len(best_moves), len(cakes), scoreboard.score])
                
                if (len(best_moves) == len(cakes) - current_state.cake_offset + len(current_state.table.get_plates_on_table())) and len(best_moves) > 0:
                    for move in best_moves:
                        new_state = apply_move(current_state, move, cakes)
                        
                        board = new_state.board
                        table = new_state.table
                        cake_offset = new_state.cake_offset
                        scoreboard = Scoreboard(screen)
                        scoreboard.score = new_state.scoreboard.score

                        board_renderer.board = board
                        table_renderer.table = table
                        plate_renderer.board = board
                        plate_renderer.table = table

                        screen.fill((200, 200, 250))
                        board_renderer.draw(screen)
                        table_renderer.draw(screen)
                        plate_renderer.draw(screen)
                        scoreboard.draw()
                        pygame.display.flip()

                        if visualize:
                            pygame.time.delay(2000)

                        current_state = new_state

                elif best_moves:
                    next_move = best_moves[0]
                    new_state = apply_move(current_state, next_move, cakes)
                    
                    board = new_state.board
                    table = new_state.table
                    cake_offset = new_state.cake_offset
                    scoreboard = Scoreboard(screen)
                    scoreboard.score = new_state.scoreboard.score

                    board_renderer.board = board
                    table_renderer.table = table
                    plate_renderer.board = board
                    plate_renderer.table = table

                    if visualize:
                        pygame.time.delay(2000)

                else:
                    print("No valid move found. Ending MonteCarloPlaying state.")
                    game_state = "GameOver"

                pygame.display.flip()

            case "GreedyMenu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        #+sys.exit()
                    action = greedy_menu.handle_event(event)
                    if action == "start_1":
                        visualize = False
                        game_state = "GreedyPlaying"
                    elif action == "start_2":
                        visualize = True
                        game_state = "GreedyPlaying"
                    elif action == "back":
                        game_state = "AIMenu"
                greedy_menu.draw()
                pygame.display.flip()
            
            case "GreedyPlaying":
                screen.fill((200, 200, 250))
                board_renderer.draw(screen)
                table_renderer.draw(screen)
                plate_renderer.draw(screen)
                scoreboard.draw()
                pygame.display.flip()

                current_state = State(board, table, cake_offset, scoreboard)
                
                start_time = time.perf_counter()
                best_moves, nodes_visited = greedy_solver(current_state,  cakes)
                end_time = time.perf_counter()

                time_taken = end_time - start_time

                csv_file_path = "results/greedy_metrics.csv"
                file_exists = os.path.isfile(csv_file_path)

                if not visualize:
                    with open("results/greedy_metrics.csv", "a", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        if not file_exists:
                            writer.writerow(["Time Taken", "Nodes Visited", "Best Moves Count", "Cakes Count", "Score"])
                        writer.writerow([time_taken, nodes_visited, len(best_moves), len(cakes), scoreboard.score])
                
                if (len(best_moves) == len(cakes) - current_state.cake_offset + len(current_state.table.get_plates_on_table())) and len(best_moves) > 0:
                    for move in best_moves:
                        new_state = apply_move(current_state, move, cakes)
                        
                        board = new_state.board
                        table = new_state.table
                        cake_offset = new_state.cake_offset
                        scoreboard = Scoreboard(screen)
                        scoreboard.score = new_state.scoreboard.score

                        board_renderer.board = board
                        table_renderer.table = table
                        plate_renderer.board = board
                        plate_renderer.table = table

                        screen.fill((200, 200, 250))
                        board_renderer.draw(screen)
                        table_renderer.draw(screen)
                        plate_renderer.draw(screen)
                        scoreboard.draw()
                        pygame.display.flip()

                        if visualize:
                            pygame.time.delay(2000)

                        current_state = new_state

                elif best_moves:
                    next_move = best_moves[0]
                    new_state = apply_move(current_state, next_move, cakes)
                    
                    board = new_state.board
                    table = new_state.table
                    cake_offset = new_state.cake_offset
                    scoreboard = Scoreboard(screen)
                    scoreboard.score = new_state.scoreboard.score

                    board_renderer.board = board
                    table_renderer.table = table
                    plate_renderer.board = board
                    plate_renderer.table = table

                    if visualize:
                        pygame.time.delay(2000)

                else:
                    print("No valid move found. Ending GreedyPlaying state.")
                    game_state = "GameOver"

                pygame.display.flip()

            case "A*Menu":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        #+sys.exit()
                    action = a_menu.handle_event(event)
                    adjust = a_menu.handle_int_button_event(event)
                    if action == "start_1":
                        visualize = False
                        game_state = "A*Playing"
                        algorithm_iterations, algorithm_depth = adjust
                    elif action == "start_2":
                        visualize = True
                        game_state = "A*Playing"
                        algorithm_iterations, algorithm_depth = adjust
                    elif action == "back":
                        game_state = "AIMenu"
                a_menu.draw()
                pygame.display.flip()
            

            case "A*Playing":
                screen.fill((200, 200, 250))
                board_renderer.draw(screen)
                table_renderer.draw(screen)
                plate_renderer.draw(screen)
                scoreboard.draw()
                pygame.display.flip()

                current_state = State(board, table, cake_offset, scoreboard)
                
                start_time = time.perf_counter()
                best_moves, nodes_visited =  a_star_solver(current_state, cakes, slice_count, algorithm_depth, algorithm_iterations)
                end_time = time.perf_counter()

                time_taken = end_time - start_time

                csv_file_path = "results/a_star_metrics.csv"
                file_exists = os.path.isfile(csv_file_path)

                if not visualize:
                    with open("results/a_star_metrics.csv", "a", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        if not file_exists:
                            writer.writerow(["Time Taken", "Nodes Visited", "Algorithm Depth", "Algorithm Iterations", "Best Moves Count", "Cakes Count", "Score"])
                        writer.writerow([time_taken, nodes_visited, algorithm_depth, algorithm_iterations, len(best_moves), len(cakes), scoreboard.score])
                
                if (len(best_moves) == len(cakes) - current_state.cake_offset + len(current_state.table.get_plates_on_table())) and len(best_moves) > 0:
                    for move in best_moves:
                        new_state = apply_move(current_state, move, cakes)
                        
                        board = new_state.board
                        table = new_state.table
                        cake_offset = new_state.cake_offset
                        scoreboard = Scoreboard(screen)
                        scoreboard.score = new_state.scoreboard.score

                        board_renderer.board = board
                        table_renderer.table = table
                        plate_renderer.board = board
                        plate_renderer.table = table

                        screen.fill((200, 200, 250))
                        board_renderer.draw(screen)
                        table_renderer.draw(screen)
                        plate_renderer.draw(screen)
                        scoreboard.draw()
                        pygame.display.flip()

                        if visualize:
                            pygame.time.delay(2000)

                        current_state = new_state

                elif best_moves:
                    next_move = best_moves[0]
                    new_state = apply_move(current_state, next_move, cakes)
                    
                    board = new_state.board
                    table = new_state.table
                    cake_offset = new_state.cake_offset
                    scoreboard = Scoreboard(screen)
                    scoreboard.score = new_state.scoreboard.score

                    board_renderer.board = board
                    table_renderer.table = table
                    plate_renderer.board = board
                    plate_renderer.table = table

                    if visualize:
                        pygame.time.delay(2000)

                else:
                    print("No valid move found. Ending A*Playing state.")
                    game_state = "GameOver"

                pygame.display.flip()

            case "Playing":
                clock = pygame.time.Clock()
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if pause_button_rect.collidepoint(event.pos):
                            current_state=State(board, table, cake_offset, scoreboard)
                            print(heuristic(current_state,cakes,slice_count))
                            game_state = "Paused"
                        elif hint_button_rect.collidepoint(event.pos):
                            current_state = State(board, table, cake_offset, scoreboard)
                            best_move = hint_solver(current_state, helper_algorithm, cakes, slice_count)
                            hint_move = best_move
                        elif not plate_is_selected:
                            pos = pygame.mouse.get_pos()
                            selected_plate = handle_plate_selection(pos, selected_plate, board, table, board_side_margin, board_top_margin, cell_size)
                            if selected_plate == "Placed":
                                selected_plate = None
                                hint_move = None
                

                if table.has_no_plates():
                    cake_offset = table.get_plates(cakes, cake_offset)
                
                screen.fill((200, 200, 250))

                board_renderer.draw(screen, selected_plate)
                table_renderer.draw(screen)
                plate_renderer.draw(screen, selected_plate)

                plate_padding = plate_renderer.spacing
                if hint_move is not None:
                    draw_hint_indicator(screen, hint_move, cell_size, board_side_margin, board_top_margin, table_x, table_y, plate_padding)

                board.clean_board(scoreboard)

                scoreboard.draw()
                draw_pause_button(screen, pause_button_rect, menu.button_font)
                draw_hint_button(screen, hint_button_rect, menu.button_font)

                if len(cakes) - cake_offset == 0 and table.has_no_plates():
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    game_state = "GameOver"
                
                pygame.display.flip()
            

            case "Paused":
                continue_button_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 40, 300, 60)
                leave_button_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 40, 300, 60)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if continue_button_rect.collidepoint(event.pos):
                            game_state = "Playing"
                        elif leave_button_rect.collidepoint(event.pos):
                            initialize_game()
                            game_state = "Menu"
                
                overlay = pygame.Surface((screen_width, screen_height))
                overlay.fill((200, 200, 250))
                screen.blit(overlay, (0, 0))
                
                mouse_pos = pygame.mouse.get_pos()
                
                if continue_button_rect.collidepoint(mouse_pos):
                    continue_bg = (200, 150, 170)
                else:
                    continue_bg = (235, 182, 203)
                
                if leave_button_rect.collidepoint(mouse_pos):
                    leave_bg = (200, 150, 170)
                else:
                    leave_bg = (235, 182, 203)
                
                pygame.draw.rect(screen, continue_bg, continue_button_rect, border_radius=10)
                pygame.draw.rect(screen, (255, 255, 255), continue_button_rect, 3, border_radius=10)
                pygame.draw.rect(screen, leave_bg, leave_button_rect, border_radius=10)
                pygame.draw.rect(screen, (255, 255, 255), leave_button_rect, 3, border_radius=10)
                
                continue_text = menu.button_font.render("Continue", True, (255, 255, 255))
                leave_text = menu.button_font.render("Leave", True, (255, 255, 255))
                continue_text_rect = continue_text.get_rect(center=continue_button_rect.center)
                leave_text_rect = leave_text.get_rect(center=leave_button_rect.center)
                screen.blit(continue_text, continue_text_rect)
                screen.blit(leave_text, leave_text_rect)
                
                pygame.display.flip()
        

            case "GameOver":
                game_over_menu = Menu(screen, "GameOver", scoreboard.score)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        #+sys.exit()

                    action = game_over_menu.handle_event(event)
                    
                    if action == "menu":
                        game_state = "Menu"
                        initialize_game()
                game_over_menu.draw()
                pygame.display.flip()
    #____________________________ MAIN LOOP ______________________________#
    
    pygame.quit()


if __name__ == "__main__":
    main()


