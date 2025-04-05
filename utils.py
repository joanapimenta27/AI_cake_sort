import pygame
import math
import random

from plate import Plate
from slice import Slice
from slice_merger import merge_slices_between_plates

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

def draw_pause_button(screen, pause_rect, button_font):
    mouse_pos = pygame.mouse.get_pos()
    if pause_rect.collidepoint(mouse_pos):
        bg_color = (200, 150, 170)
    else:
        bg_color = (235, 182, 203)
    
    pygame.draw.rect(screen, bg_color, pause_rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), pause_rect, 3, border_radius=10)
    
    bar_width = pause_rect.width // 5
    bar_height = int(pause_rect.height * 0.6)
    gap = bar_width // 2
    
    bar1 = pygame.Rect(
        pause_rect.centerx - gap - bar_width,
        pause_rect.centery - bar_height // 2,
        bar_width,
        bar_height
    )
    bar2 = pygame.Rect(
        pause_rect.centerx + gap,
        pause_rect.centery - bar_height // 2,
        bar_width,
        bar_height
    )
    pygame.draw.rect(screen, (255, 255, 255), bar1)
    pygame.draw.rect(screen, (255, 255, 255), bar2)

def possible_moves(state):

    moves = []
    board = state.board
    table = state.table

    for i, plate in enumerate(table.plates):
        if plate is None:
            continue
        for row in range(board.rows):
            for col in range(board.cols):
                if board.is_valid_tile(row, col):
                    moves.append((i, row, col))
    
    return moves



def apply_move(state, move):
    
    new_state = state.copy()
    table_index, row, col = move
    plate = new_state.table.plates[table_index]
    new_state.board.place_item(row, col, plate)
    new_state.table.remove_plate(table_index)

    if new_state.table.has_no_plates() and len(new_state.cakes) > 0:
        new_state.table.get_plates(new_state.cakes)
    
    board = new_state.board
    adjacent_plates = board.get_adjacent_plates(row, col)
    merge_slices_between_plates(adjacent_plates, plate)
    board.clean_board(new_state.scoreboard, delay=False)
    return new_state