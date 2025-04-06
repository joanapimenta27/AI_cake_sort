import pygame
import sys


class Menu:
    def __init__(self, screen, menu_type = "Start", score = 0):
        self.screen = screen
        self.menu_type = menu_type
        self.width, self.height = screen.get_size()
        self.font = pygame.font.SysFont("comicsans", 100)
        self.info_font = pygame.font.SysFont("comicsans", 50)
        self.button_font = pygame.font.SysFont("comicsans", 30)
        self.depth = 2
        self.iteractions = 300
 


        match menu_type:
            case "Start":
                self.title = self.font.render("Cake Sort", True, (235, 182, 203))
                self.start_button = pygame.Rect(self.width // 2 - 150, self.height // 2 - 50, 300, 60)
                self.ai_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 30, 300, 60)
                self.settings_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 110, 300, 60)
                self.quit_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 190, 300, 60)
            case "SettingsMenu":
                self.rows = 3
                self.columns = 3
                self.cakes = 20
                self.slices = 6
                self.plates = 3
                self.helper_list = ["BFS", "DFS", "Greedy", "A*", "Monte Carlo"]
                self.helper_idx = 0
                self.title = self.font.render("Settings", True, (235, 182, 203))
                self.number_of_rows = pygame.Rect(self.width // 2 - 325, self.height // 2 - 50, 300, 60)
                self.info_rows = self.info_font.render("Rows", True, (235, 182, 203))
                self.number_of_columns = pygame.Rect(self.width // 2 + 25, self.height // 2 - 50, 300, 60)
                self.info_columns = self.info_font.render("Columns", True, (235, 182, 203))
                self.number_of_cakes = pygame.Rect(self.width // 2 - 325, self.height // 2 + 70, 300, 60)
                self.info_cakes = self.info_font.render("Cakes", True, (235, 182, 203))
                self.number_of_slices = pygame.Rect(self.width // 2 + 25, self.height // 2 + 70, 300, 60)
                self.info_slices = self.info_font.render("Slices", True, (235, 182, 203))
                self.number_of_plates_on_table = pygame.Rect(self.width // 2 - 325, self.height // 2 + 190, 300, 60)
                self.info_plates = self.info_font.render("Plates in Table", True, (235, 182, 203))
                self.helper_algorithm = pygame.Rect(self.width // 2 + 25, self.height // 2 + 190, 300, 60)
                self.info_helper = self.info_font.render("Helper Algorithm", True, (235, 182, 203))
                self.back_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 310, 300, 60)
            case "AIMenu":
                self.title = self.font.render("AI Menu", True, (235, 182, 203))
                self.dfs_button = pygame.Rect(self.width // 2 - 325, self.height // 2 - 50, 300, 60)
                self.bfs_button = pygame.Rect(self.width // 2 + 25, self.height // 2 - 50, 300, 60)
                self.greedy_button = pygame.Rect(self.width // 2 - 325, self.height // 2 + 30, 300, 60)
                self.a_start_button = pygame.Rect(self.width // 2 + 25, self.height // 2 + 30, 300, 60)
                self.monte_carlo_button = pygame.Rect(self.width // 2 - 325, self.height // 2 + 110, 300, 60)
                self.back_button = pygame.Rect(self.width // 2 + 25, self.height // 2 + 110, 300, 60)
            case "BFSMenu":
                self.title = self.font.render("BFS Menu", True, (235, 182, 203))
                self.info = self.info_font.render("Depth", True, (235, 182, 203))
                self.start_1_button = pygame.Rect(self.width // 2 - 325, self.height // 2 - 50, 300, 60)
                self.start_2_button = pygame.Rect(self.width // 2 + 25, self.height // 2 - 50, 300, 60)
                self.depth_button = pygame.Rect(self.width // 2 - 325, self.height // 2 + 30, 300, 60)
                self.back_button = pygame.Rect(self.width // 2 + 25, self.height // 2 + 30, 300, 60)
            case "DFSMenu":
                self.title = self.font.render("DFS Menu", True, (235, 182, 203))
                self.info = self.info_font.render("DEPTH", True, (235, 182, 203))
                self.start_1_button = pygame.Rect(self.width // 2 - 325, self.height // 2 - 50, 300, 60)
                self.start_2_button = pygame.Rect(self.width // 2 + 25, self.height // 2 - 50, 300, 60)
                self.depth_button = pygame.Rect(self.width // 2 - 325, self.height // 2 + 30, 300, 60)
                self.back_button = pygame.Rect(self.width // 2 + 25, self.height // 2 + 30, 300, 60)   
            case "GreedyMenu":
                self.title = self.font.render("Greedy Menu", True, (235, 182, 203))
                self.start_1_button = pygame.Rect(self.width // 2 - 325, self.height // 2 - 50, 300, 60)
                self.start_2_button = pygame.Rect(self.width // 2 + 25, self.height // 2 - 50, 300, 60)
                self.back_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 30, 300, 60) 
            case "A*Menu":
                self.depth = 30
                self.title = self.font.render("A* Menu", True, (235, 182, 203))
                self.info = self.info_font.render("Iterations", True, (235, 182, 203))
                self.info2 = self.info_font.render("Depth/Iteration", True, (235, 182, 203))
                self.start_1_button = pygame.Rect(self.width // 2 - 325, self.height // 2 - 50, 300, 60)
                self.start_2_button = pygame.Rect(self.width // 2 + 25, self.height // 2 - 50, 300, 60)
                self.depth_button = pygame.Rect(self.width // 2 + 25, self.height // 2 + 30, 300, 60)
                self.iteractions_button = pygame.Rect(self.width // 2 - 325, self.height // 2 + 30, 300, 60)
                self.back_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 150, 300, 60)                 
            case "MonteCarloMenu":
                self.depth = 30
                self.title = self.font.render("Monte Carlo Menu", True, (235, 182, 203))
                self.info = self.info_font.render("Iterations", True, (235, 182, 203))
                self.info2 = self.info_font.render("Depth/Iteration", True, (235, 182, 203))
                self.start_1_button = pygame.Rect(self.width // 2 - 325, self.height // 2 - 50, 300, 60)
                self.start_2_button = pygame.Rect(self.width // 2 + 25, self.height // 2 - 50, 300, 60)
                self.depth_button = pygame.Rect(self.width // 2 + 25, self.height // 2 + 30, 300, 60)
                self.iteractions_button = pygame.Rect(self.width // 2 - 325, self.height // 2 + 30, 300, 60)
                self.back_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 150, 300, 60)
            case "GameOver":
                self.title = self.font.render("Game Over", True, (235, 182, 203))
                self.score = self.font.render(f"Score: {score}", True, (235, 182, 203))
                self.mainmenu_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 110, 300, 60)


        # Background
        self.background = pygame.image.load("assets/cake_background.webp")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Draw Title
        title_rect = self.title.get_rect(center=(self.width // 2, (self.height * 3) // 10))
        self.screen.blit(self.title, title_rect)

        # Draw Buttons
        match self.menu_type:
            case "Start":
                self.draw_button(self.start_button, "Play")
                self.draw_button(self.ai_button, "AI")
                self.draw_button(self.settings_button, "Settings")
                self.draw_button(self.quit_button, "Quit")
            case "SettingsMenu":
                self.draw_changable_buttons(self.number_of_rows, self.rows)
                info_rows_rect = self.info_rows.get_rect(center=(self.width // 2 - 180, self.height // 2 - 70))
                self.screen.blit(self.info_rows, info_rows_rect)
                self.draw_changable_buttons(self.number_of_columns, self.columns)
                info_columns_rect = self.info_columns.get_rect(center=(self.width // 2 + 180, self.height // 2 - 70))
                self.screen.blit(self.info_columns, info_columns_rect)
                self.draw_changable_buttons(self.number_of_cakes, self.cakes)
                info_cakes_rect = self.info_cakes.get_rect(center=(self.width // 2 - 180, self.height // 2 + 50))
                self.screen.blit(self.info_cakes, info_cakes_rect)
                self.draw_changable_buttons(self.number_of_slices, self.slices)
                info_slices_rect = self.info_slices.get_rect(center=(self.width // 2 + 180, self.height // 2 + 50))
                self.screen.blit(self.info_slices, info_slices_rect)
                self.draw_changable_buttons(self.number_of_plates_on_table, self.plates)
                info_plates_rect = self.info_plates.get_rect(center=(self.width // 2 - 180, self.height // 2 + 170))
                self.screen.blit(self.info_plates, info_plates_rect)
                self.draw_changable_buttons(self.helper_algorithm, self.helper_list[self.helper_idx])
                info_helper_rect = self.info_helper.get_rect(center=(self.width // 2 + 180, self.height // 2 + 170))
                self.screen.blit(self.info_helper, info_helper_rect)
                self.draw_button(self.back_button, "Back")
            case "AIMenu":
                self.draw_button(self.dfs_button, "DFS")
                self.draw_button(self.bfs_button, "BFS")
                self.draw_button(self.greedy_button, "Greedy")
                self.draw_button(self.a_start_button, "A*")
                self.draw_button(self.monte_carlo_button, "Monte Carlo")
                self.draw_button(self.back_button, "Back")
            case "BFSMenu":
                self.draw_button(self.start_1_button, "Start Machine Mode")
                self.draw_button(self.start_2_button, "Start Spectator Mode")
                self.draw_changable_buttons(self.depth_button, self.depth)
                self.draw_button(self.back_button, "Back")
                info_rect = self.info.get_rect(center=(self.width // 2 - 180, self.height // 2 + 110))
                self.screen.blit(self.info, info_rect)
            case "DFSMenu":
                self.draw_button(self.start_1_button, "Start Machine Mode")
                self.draw_button(self.start_2_button, "Start Spectator Mode")
                self.draw_changable_buttons(self.depth_button, self.depth)
                self.draw_button(self.back_button, "Back")
                info_rect = self.info.get_rect(center=(self.width // 2 - 180, self.height // 2 + 110))
                self.screen.blit(self.info, info_rect)
            case "GreedyMenu":
                self.draw_button(self.start_1_button, "Start Machine Mode")
                self.draw_button(self.start_2_button, "Start Spectator Mode")
                self.draw_button(self.back_button, "Back")
            case "A*Menu":
                self.draw_button(self.start_1_button, "Start Machine Mode")
                self.draw_button(self.start_2_button, "Start Spectator Mode")
                self.draw_changable_buttons(self.depth_button, self.depth)
                self.draw_changable_buttons(self.iteractions_button, self.iteractions)
                self.draw_button(self.back_button, "Back")
                info_rect = self.info.get_rect(center=(self.width // 2 - 175, self.height // 2 + 110))
                self.screen.blit(self.info, info_rect)
                info_rect2 = self.info2.get_rect(center=(self.width // 2 + 175, self.height // 2 + 110))
                self.screen.blit(self.info2, info_rect2)
            case "MonteCarloMenu":
                self.draw_button(self.start_1_button, "Start Machine Mode")
                self.draw_button(self.start_2_button, "Start Spectator Mode")
                self.draw_changable_buttons(self.depth_button, self.depth)
                self.draw_changable_buttons(self.iteractions_button, self.iteractions)
                self.draw_button(self.back_button, "Back")
                info_rect = self.info.get_rect(center=(self.width // 2 - 175, self.height // 2 + 110))
                self.screen.blit(self.info, info_rect)
                info_rect2 = self.info2.get_rect(center=(self.width // 2 + 175, self.height // 2 + 110))
                self.screen.blit(self.info2, info_rect2)
            case "GameOver":
                score_rect = self.score.get_rect(center=(self.width // 2, (self.height * 3) // 10 + 70) )
                self.screen.blit(self.score, score_rect)
                self.draw_button(self.mainmenu_button, "Main Menu")

    def draw_button(self, rect, text):
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            button_color = (200, 150, 170)
        else:
            button_color = (235, 182, 203)
        pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=10)
        button_text = self.button_font.render(text, True, (255, 255, 255))
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            match self.menu_type:
                case "Start":
                    if self.start_button.collidepoint(event.pos):
                        return "start"
                    elif self.ai_button.collidepoint(event.pos):
                        return "aiMenu"
                    elif self.settings_button.collidepoint(event.pos):
                        return "settings"
                    elif self.quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                case "SettingsMenu":
                    if self.back_button.collidepoint(event.pos):
                        return "back"
                case "AIMenu":
                    if self.dfs_button.collidepoint(event.pos):
                        return "DFS"
                    elif self.bfs_button.collidepoint(event.pos):
                        return "BFS"
                    elif self.greedy_button.collidepoint(event.pos):
                        return "Greedy"
                    elif self.a_start_button.collidepoint(event.pos):
                        return "AStar"
                    elif self.monte_carlo_button.collidepoint(event.pos):
                        return "Monte Carlo"
                    elif self.back_button.collidepoint(event.pos):
                        return "back"
                case "BFSMenu":
                    if self.start_1_button.collidepoint(event.pos):
                        return "start_1"
                    elif self.start_2_button.collidepoint(event.pos):
                        return "start_2"
                    elif self.back_button.collidepoint(event.pos):
                        return "back"
                case "DFSMenu":
                    if self.start_1_button.collidepoint(event.pos):
                        return "start_1"
                    elif self.start_2_button.collidepoint(event.pos):
                        return "start_2"
                    elif self.back_button.collidepoint(event.pos):
                        return "back"
                case "GreedyMenu":
                    if self.start_1_button.collidepoint(event.pos):
                        return "start_1"
                    elif self.start_2_button.collidepoint(event.pos):
                        return "start_2"
                    elif self.back_button.collidepoint(event.pos):
                        return "back"
                case "A*Menu":
                    if self.start_1_button.collidepoint(event.pos):
                        return "start_1"
                    elif self.start_2_button.collidepoint(event.pos):
                        return "start_2"
                    elif self.back_button.collidepoint(event.pos):
                        return "back"
                case "MonteCarloMenu":
                    if self.start_1_button.collidepoint(event.pos):
                        return "start_1"
                    elif self.start_2_button.collidepoint(event.pos):
                        return "start_2"
                    elif self.back_button.collidepoint(event.pos):
                        return "back"
                case "GameOver":
                    if self.mainmenu_button.collidepoint(event.pos):
                        return "menu"
        return None


    def draw_changable_buttons(self, rect, value):
        default_bg = (235, 182, 203)
        hover_bg = (200, 150, 170)
        
        third_width = rect.width // 3
        left_rect = pygame.Rect(rect.left, rect.top, third_width, rect.height)
        center_rect = pygame.Rect(rect.left + third_width, rect.top, third_width, rect.height)
        right_rect = pygame.Rect(rect.right - third_width, rect.top, third_width, rect.height)
    
        pygame.draw.rect(self.screen, default_bg, rect, border_radius=10)
        
        mouse_pos = pygame.mouse.get_pos()
        
        if left_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, hover_bg, left_rect, border_radius=10)
        
        if right_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, hover_bg, right_rect, border_radius=10)
        
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=10)
        
        left_text = self.button_font.render("<", True, (255, 255, 255))
        right_text = self.button_font.render(">", True, (255, 255, 255))
        value_text = self.button_font.render(str(value), True, (255, 255, 255))
        
        left_text_rect = left_text.get_rect(center=left_rect.center)
        right_text_rect = right_text.get_rect(center=right_rect.center)
        value_text_rect = value_text.get_rect(center=rect.center)
        
        self.screen.blit(left_text, left_text_rect)
        self.screen.blit(value_text, value_text_rect)
        self.screen.blit(right_text, right_text_rect)
    
    def handle_int_button_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            match self.menu_type:
                case "SettingsMenu":
                    third_width_rows = self.number_of_rows.width // 3
                    left_area_rows = pygame.Rect(self.number_of_rows.left, self.number_of_rows.top, third_width_rows, self.number_of_rows.height)
                    right_area_rows = pygame.Rect(self.number_of_rows.right - third_width_rows, self.number_of_rows.top, third_width_rows, self.number_of_rows.height)
                    if left_area_rows.collidepoint(mouse_pos):
                        self.rows = max(2, self.rows - 1)
                    elif right_area_rows.collidepoint(mouse_pos):
                        self.rows = min(8, self.rows + 1)
                    third_width_columns = self.number_of_columns.width // 3
                    left_area_columns = pygame.Rect(self.number_of_columns.left, self.number_of_columns.top, third_width_columns, self.number_of_columns.height)
                    right_area_columns = pygame.Rect(self.number_of_columns.right - third_width_columns, self.number_of_columns.top, third_width_columns, self.number_of_columns.height)
                    if left_area_columns.collidepoint(mouse_pos):
                        self.columns = max(2, self.columns - 1)
                    elif right_area_columns.collidepoint(mouse_pos):
                        self.columns = min(8, self.columns + 1)
                    third_width_cakes = self.number_of_cakes.width // 3
                    left_area_cakes = pygame.Rect(self.number_of_cakes.left, self.number_of_cakes.top, third_width_cakes, self.number_of_cakes.height)
                    right_area_cakes = pygame.Rect(self.number_of_cakes.right - third_width_cakes, self.number_of_cakes.top, third_width_cakes, self.number_of_cakes.height)
                    if left_area_cakes.collidepoint(mouse_pos):
                        self.cakes = max(3, self.cakes - 2)
                    elif right_area_cakes.collidepoint(mouse_pos):
                        self.cakes = min(200, self.cakes + 2)
                    third_width_slices = self.number_of_slices.width // 3
                    left_area_slices = pygame.Rect(self.number_of_slices.left, self.number_of_slices.top, third_width_slices, self.number_of_slices.height)
                    right_area_slices = pygame.Rect(self.number_of_slices.right - third_width_slices, self.number_of_slices.top, third_width_slices, self.number_of_slices.height)
                    if left_area_slices.collidepoint(mouse_pos):
                        self.slices = max(2, self.slices - 1)
                    elif right_area_slices.collidepoint(mouse_pos):
                        self.slices = min(8, self.slices + 1)
                    third_width_plates = self.number_of_plates_on_table.width // 3
                    left_area_plates = pygame.Rect(self.number_of_plates_on_table.left, self.number_of_plates_on_table.top, third_width_plates, self.number_of_plates_on_table.height)
                    right_area_plates = pygame.Rect(self.number_of_plates_on_table.right - third_width_plates, self.number_of_plates_on_table.top, third_width_plates, self.number_of_plates_on_table.height)
                    if left_area_plates.collidepoint(mouse_pos):
                        self.plates = max(1, self.plates - 1)
                    elif right_area_plates.collidepoint(mouse_pos):
                        self.plates = min(5, self.plates + 1)
                    third_width_helper = self.helper_algorithm.width // 3
                    left_area_helper = pygame.Rect(self.helper_algorithm.left, self.helper_algorithm.top, third_width_helper, self.helper_algorithm.height)
                    right_area_helper = pygame.Rect(self.helper_algorithm.right - third_width_helper, self.helper_algorithm.top, third_width_helper, self.helper_algorithm.height)
                    if left_area_helper.collidepoint(mouse_pos):
                        self.helper_idx = (self.helper_idx - 1) % len(self.helper_list)
                    elif right_area_helper.collidepoint(mouse_pos):
                        self.helper_idx = (self.helper_idx + 1) % len(self.helper_list)
                    return self.rows, self.columns, self.cakes, self.slices, self.plates, self.helper_list[self.helper_idx]
                case "BFSMenu":
                    third_width = self.depth_button.width // 3
                    left_area = pygame.Rect(self.depth_button.left, self.depth_button.top, third_width, self.depth_button.height)
                    right_area = pygame.Rect(self.depth_button.right - third_width, self.depth_button.top, third_width, self.depth_button.height)
                    if left_area.collidepoint(mouse_pos):
                        self.depth = max(1, self.depth - 1)
                    elif right_area.collidepoint(mouse_pos):
                        self.depth = min(7, self.depth + 1)
                case "DFSMenu":
                    third_width = self.depth_button.width // 3
                    left_area = pygame.Rect(self.depth_button.left, self.depth_button.top, third_width, self.depth_button.height)
                    right_area = pygame.Rect(self.depth_button.right - third_width, self.depth_button.top, third_width, self.depth_button.height)
                    if left_area.collidepoint(mouse_pos):
                        self.depth = max(1, self.depth - 1)
                    elif right_area.collidepoint(mouse_pos):
                        self.depth = min(7, self.depth + 1)     
                case "MonteCarloMenu":
                    third_width = self.depth_button.width // 3
                    left_area = pygame.Rect(self.depth_button.left, self.depth_button.top, third_width, self.depth_button.height)
                    right_area = pygame.Rect(self.depth_button.right - third_width, self.depth_button.top, third_width, self.depth_button.height)
                    if left_area.collidepoint(mouse_pos):
                        self.depth = max(1, self.depth - 1)
                    elif right_area.collidepoint(mouse_pos):
                        self.depth = min(50, self.depth + 1)
                    third_width2 = self.iteractions_button.width // 3
                    left_area2 = pygame.Rect(self.iteractions_button.left, self.iteractions_button.top, third_width2, self.iteractions_button.height)
                    right_area2 = pygame.Rect(self.iteractions_button.right - third_width2, self.iteractions_button.top, third_width2, self.iteractions_button.height)
                    if left_area2.collidepoint(mouse_pos):
                        self.iteractions = max(100, self.iteractions - 100)
                    elif right_area2.collidepoint(mouse_pos):
                        self.iteractions = min(5000, self.iteractions + 100)
                    return self.iteractions, self.depth
                case "A*Menu":
                    third_width = self.depth_button.width // 3
                    left_area = pygame.Rect(self.depth_button.left, self.depth_button.top, third_width, self.depth_button.height)
                    right_area = pygame.Rect(self.depth_button.right - third_width, self.depth_button.top, third_width, self.depth_button.height)
                    if left_area.collidepoint(mouse_pos):
                        self.depth = max(1, self.depth - 1)
                    elif right_area.collidepoint(mouse_pos):
                        self.depth = min(50, self.depth + 1)
                    third_width2 = self.iteractions_button.width // 3
                    left_area2 = pygame.Rect(self.iteractions_button.left, self.iteractions_button.top, third_width2, self.iteractions_button.height)
                    right_area2 = pygame.Rect(self.iteractions_button.right - third_width2, self.iteractions_button.top, third_width2, self.iteractions_button.height)
                    if left_area2.collidepoint(mouse_pos):
                        self.iteractions = max(100, self.iteractions - 100)
                    elif right_area2.collidepoint(mouse_pos):
                        self.iteractions = min(5000, self.iteractions + 100)
                    return self.iteractions, self.depth
        
            return self.depth
    
   