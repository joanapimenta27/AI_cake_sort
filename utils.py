import pygame
import math
import random

from plate import Plate
from slice import Slice

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

def generate_cakes(cake_data, slice_count, num_cakes, seed=None):
    if seed is not None:
        random.seed(seed)

    cakes = []
    
    groups = len(cake_data) - 1  
    group_size = num_cakes / groups

    for i in range(num_cakes):
        group = int(i / group_size)
        if group >= groups:
            group = groups - 1
        
        available_types = group + 2
        if available_types > len(cake_data):
            available_types = len(cake_data)
        
        number_of_slices = random.randint(1, slice_count - 1)
        cake = Plate()     
        
        for i in range(number_of_slices):
            flavor = random.randint(0, available_types-1)
            slice = Slice(flavor)
            cake.add_slice(slice)
        
        cakes.append(cake)
    
    return cakes