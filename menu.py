import pygame
import sys

from settings import SettingsMenu

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.SysFont("comicsans", 100)
        self.button_font = pygame.font.SysFont("comicsans", 30)

        self.title = self.font.render("Cake Sort", True, (235, 182, 203))
        self.start_button = pygame.Rect(self.width // 2 - 150, self.height // 2 - 50, 300, 60)
        self.settings_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 30, 300, 60)
        self.quit_button = pygame.Rect(self.width // 2 - 150, self.height // 2 + 110, 300, 60)

        # Background
        self.background = pygame.image.load("assets/cake_background.webp")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Draw Title
        title_rect = self.title.get_rect(center=(self.width // 2, (self.height * 3) // 10))
        self.screen.blit(self.title, title_rect)

        # Draw Buttons
        self.draw_button(self.start_button, "Start")
        self.draw_button(self.settings_button, "Settings")
        self.draw_button(self.quit_button, "Quit")

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, (235, 182, 203), rect, border_radius=10)
        pygame.draw.rect(self.screen, (255,255,255), rect, 3, border_radius=10)

        button_text = self.button_font.render(text, True, (255,255,255))
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                return "start"
            elif self.settings_button.collidepoint(event.pos):
                return "settings"
            elif self.quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
        return None
    
   