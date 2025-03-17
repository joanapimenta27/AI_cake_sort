import pygame

class Scoreboard:
    def __init__(self, screen, font_size=50, color=(255, 255, 255)):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.color = color
        self.font = pygame.font.SysFont("comicsans", font_size, bold=True)
        self.score = 0

        # Add background and border
        self.bg_color = (235, 182, 203)  # Light pink
        self.border_color = (255, 170, 180)  # Darker pink
        self.border_width = 4

    def update_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

    def draw(self):
        score_text = self.font.render(f"Score: {self.score}", True, self.color)
        text_rect = score_text.get_rect(center=(self.width // 2, 30))

        # Draw background with border
        bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10)
        pygame.draw.rect(self.screen, self.border_color, bg_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.bg_color, bg_rect.inflate(-self.border_width, -self.border_width), border_radius=10)

        # Draw text
        self.screen.blit(score_text, text_rect)
