import pygame
import sys

class SettingsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.SysFont("comicsans", 60)
        self.button_font = pygame.font.SysFont("comicsans", 40)

        self.back_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 100, 200, 50)

    def draw(self):
        self.screen.fill((255, 223, 186))

        # Draw Title
        title = self.font.render("Settings Coming Soon!", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 4))
        self.screen.blit(title, title_rect)

        # Draw Back Button
        pygame.draw.rect(self.screen, (240, 200, 150), self.back_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 170, 100), self.back_button, 3, border_radius=10)

        back_text = self.button_font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "back"
        return None

