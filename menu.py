import pygame
import sys

from settings import SettingsMenu

class Menu:
    def __init__(self, screen, menu_type = "Start", score = 0):
        self.screen = screen
        self.menu_type = menu_type
        self.width, self.height = screen.get_size()
        self.font = pygame.font.SysFont("comicsans", 100)
        self.info_font = pygame.font.SysFont("comicsans", 50)
        self.button_font = pygame.font.SysFont("comicsans", 30)
        self.bfs_depth = 3


        match menu_type:
            case "Start":
                self.title = self.font.render("Cake Sort", True, (235, 182, 203))
                self.start_button = pygame.Rect(self.width // 2 - 150, self.height // 2 - 50, 300, 60)
                self.ai_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 30, 300, 60)
                self.settings_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 110, 300, 60)
                self.quit_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 190, 300, 60)
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
            case "GameOver":
                self.title = self.font.render("Game Over", True, (235, 182, 203))
                self.score = self.font.render(f"Score: {score}", True, (235, 182, 203))
                self.restart_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 30, 300, 60)
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
                self.draw_button(self.start_button, "Start")
                self.draw_button(self.ai_button, "AI")
                self.draw_button(self.settings_button, "Settings")
                self.draw_button(self.quit_button, "Quit")
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
                self.draw_changable_buttons(self.depth_button, self.bfs_depth)
                self.draw_button(self.back_button, "Back")
                info_rect = self.info.get_rect(center=(self.width // 2 - 180, self.height // 2 + 110))
                self.screen.blit(self.info, info_rect)
            case "GameOver":
                score_rect = self.score.get_rect(center=(self.width // 2, (self.height * 3) // 10 + 70) )
                self.screen.blit(self.score, score_rect)
                self.draw_button(self.restart_button, "Play Again")
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
                case "AIMenu":
                    if self.dfs_button.collidepoint(event.pos):
                        return "DFS"
                    elif self.bfs_button.collidepoint(event.pos):
                        return "BFS"
                    elif self.greedy_button.collidepoint(event.pos):
                        return "Greedy"
                    elif self.a_start_button.collidepoint(event.pos):
                        return "A*"
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
                case "GameOver":
                    if self.restart_button.collidepoint(event.pos):
                        return "start"
                    elif self.mainmenu_button.collidepoint(event.pos):
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
            if self.depth_button.collidepoint(mouse_pos):
                match self.menu_type:
                    case "BFSMenu":
                        third_width = self.depth_button.width // 3
                        left_area = pygame.Rect(self.depth_button.left, self.depth_button.top, third_width, self.depth_button.height)
                        right_area = pygame.Rect(self.depth_button.right - third_width, self.depth_button.top, third_width, self.depth_button.height)
                        if left_area.collidepoint(mouse_pos):
                            self.bfs_depth = max(1, self.bfs_depth - 1)
                        elif right_area.collidepoint(mouse_pos):
                            self.bfs_depth = min(10, self.bfs_depth + 1)
    
   