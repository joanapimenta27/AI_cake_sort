import pygame

from utils import create_wedge_surface

class SliceRenderer:
    def __init__(self, cake_data_list, slice_count):
        self.slice_count = slice_count
        self.wedges = {}
        slice_angle = 360 / slice_count
        for idx, full_cake_img in enumerate(cake_data_list):
            wedges = []
            for i in range(slice_count):
                start_angle = i * slice_angle
                end_angle = (i + 1) * slice_angle + 1
                wedge_surf = create_wedge_surface(full_cake_img, start_angle, end_angle)
                wedges.append(wedge_surf)
            self.wedges[idx] = wedges


    def draw_slice(self, screen, cake_index, slice_index, plate_center_x, plate_center_y):
        wedge_surf = self.wedges[cake_index][slice_index]
        w, h = wedge_surf.get_size()

        x = plate_center_x - w // 2
        y = plate_center_y - h // 2
        screen.blit(wedge_surf, (x, y))