import pygame
import math

def create_wedge_surface(full_cake_image, start_angle_deg, end_angle_deg):

    width, height = full_cake_image.get_size()
    wedge_surf = pygame.Surface((width, height), pygame.SRCALPHA)

    cx, cy = width // 2, height // 2
    r = min(cx, cy)

    steps = 50
    angle_inc = (end_angle_deg - start_angle_deg) / steps

    points = [(cx, cy)]
    for i in range(steps + 1):
        a = math.radians(start_angle_deg + i * angle_inc)
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        points.append((x, y))

    pygame.draw.polygon(wedge_surf, (255, 255, 255, 255), points)

    wedge_surf.blit(full_cake_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return wedge_surf