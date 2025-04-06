import pygame

from slice_merger import merge_slices_between_plates

def handle_plate_selection(pos, selected_plate, board, table, board_side_margin, board_top_margin, cell_size):
    
    screen = pygame.display.get_surface()
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    table_height = cell_size + table.padding*2
    table_x = table.side_img_width
    table_y = screen_height - table_height
    table_width = screen_width - 2 * table.side_img_width


    if pos[1] >= table_y:
        plates = table.plates
        num_plates = table.max_plates
        clicked_plate = None
        if num_plates > 0:
            spacing = (table_width - cell_size*num_plates) // (num_plates + 1)
            for i, plate in enumerate(plates):
                cx = table_x + spacing + i * (cell_size + spacing)
                cy = table_y + table.padding
                if cx <= pos[0] <= cx + cell_size and cy <= pos[1] <= cy + cell_size:
                    clicked_plate = plate
                    break
        
        if clicked_plate is not None:
            if selected_plate is None:
                selected_plate = clicked_plate
            elif selected_plate is clicked_plate:
                selected_plate = None
            else:
                selected_plate = clicked_plate
        
        return selected_plate
    
    else:
        if selected_plate is not None:
            col = int((pos[0]-board_side_margin)//cell_size)
            row = int((pos[1]-board_top_margin)//cell_size)
            #PLACE A PLATE
            if board.is_valid_tile(row, col):
                board.place_item(row, col, selected_plate)
                adjacent_plates = board.get_adjacent_plates(row, col)
                merge_slices_between_plates(adjacent_plates, selected_plate)
                if selected_plate in table.plates:
                    table.remove_plate(table.plates.index(selected_plate))
                return "Placed"
        
        return selected_plate