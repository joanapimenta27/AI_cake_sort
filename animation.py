import math
import pygame

def pulsing_alpha_animation(frequency=2, base=50, amplitude=60):
    t = pygame.time.get_ticks() / 1000.0
    alpha = base + amplitude * math.sin(2 * math.pi * frequency * t)
    return max(0, min(255, int(alpha)))
