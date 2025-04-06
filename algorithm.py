from collections import deque
import copy
import random
import math
import heapq
import itertools
import time



from board import Board
from plate import Plate
from table import Table
from utils import *



def bfs_solver(initial_state, depth, cakes):
    visited = set()
    queue = deque()
    queue.append((initial_state, []))
    visited.add(initial_state)

    best_moves = []
    best_score = -float('inf')

    while queue:
        state, moves = queue.popleft()

        score = state.scoreboard.score
        if score >= best_score:
            best_score = score
            best_moves = moves
                
        if len(moves) < depth:
            for move in possible_moves(state):
                new_state = apply_move(state, move, cakes)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, moves + [move]))
    

    return best_moves



def dfs_solver(initial_state, depth, cakes):
    visited = set()
    stack = []
    stack.append((initial_state, []))
    visited.add(initial_state)

    best_moves = []
    best_score = -float('inf')
    
    while stack:
        state, moves = stack.pop()

        score = state.scoreboard.score
        if score >= best_score:
            best_score = score
            best_moves = moves

        if len(moves) < depth:
            for move in possible_moves(state):
                new_state = apply_move(state, move, cakes)
                if new_state not in visited:
                    visited.add(new_state)
                    stack.append((new_state, moves + [move]))

    return best_moves


def monte_carlo_solver(initial_state, iterations, depth, cakes):

    best_moves = []
    best_score = -float('inf')

    for i in range(iterations):
        simulation_state = initial_state.copy()
        moves_sim = []
        for _ in range(depth):
            moves = possible_moves(simulation_state)
            if not moves:
                break
            move = random.choice(moves)
            simulation_state = apply_move(simulation_state, move, cakes)
            moves_sim.append(move)

        score = simulation_state.scoreboard.score
        if score > best_score:
            best_score = score
            best_moves = moves_sim
    
    return best_moves

def greedy_solver(current_state, cakes):

    best_moves = []

    while True:
        candidate_best_move = None
        candidate_best_state = None
        candidate_best_score = float('-inf')

        moves_list = possible_moves(current_state)
        if not moves_list:
            break

        for move in moves_list:
            new_state = apply_move(current_state, move, cakes)
            new_score = new_state.scoreboard.score

            if new_score > candidate_best_score:
                candidate_best_score = new_score
                candidate_best_move = move
                candidate_best_state = new_state

        if candidate_best_move is None:
            break

        best_moves.append(candidate_best_move)
        current_state = candidate_best_state

    return best_moves

def heuristic(state, cakes, slice_count):
    board =state.board
    offset=state.cake_offset
    table=state.table

    table_plates=table.get_plates_on_table()
    board_plates=board.get_cakes_from_board()
    remain_plates = []
    combined_plates = []
    for i in range(offset, len(cakes)):
        remain_plates.append(cakes[i])
    combined_plates = table_plates + board_plates + remain_plates

    flavor_counts = {}
    flavor_counts= count_slices_by_flavor(combined_plates)

    total_complete_cakes = 0
    for flavor, count in flavor_counts.items():
        total_complete_cakes += count // slice_count

    all_slices=0
    need_plates=0
    all_slices= sum(flavor_counts.values())
    need_plates= math.ceil(all_slices / slice_count)

    return ((20*total_complete_cakes) + (len(combined_plates)-need_plates)*10 )

def state_key(state):
    board_key = tuple(
        tuple(
            tuple(slice_obj.cake_index() if slice_obj is not None else None for slice_obj in cell.slices)
            if cell is not None else None
            for cell in row
        ) for row in state.board.grid
    )
    table_key = tuple(
        tuple(slice_obj.cake_index() if slice_obj is not None else None for slice_obj in plate.slices)
        if plate is not None else None
        for plate in state.table.plates
    )
    return (board_key, table_key, state.cake_offset, state.scoreboard.score)

def a_star_solver(initial_state, cakes, slice_count, max_depth=5, max_iterations=1000):

    counter = itertools.count()  
    open_set = []

    def cost(state):
        return -state.scoreboard.score

    start_cost = cost(initial_state)
    start_priority = start_cost + heuristic(initial_state, cakes, slice_count)
    heapq.heappush(open_set, (start_priority, next(counter), initial_state, []))

    closed_set = set()
    best_path = []
    best_score = initial_state.scoreboard.score
    iterations = 0
    start_time = time.time()

    
    init_moves = possible_moves(initial_state)
    print(f"Initial moves count: {len(init_moves)}")

    while open_set and iterations < max_iterations:
        iterations += 1
        f_val, _, current_state, path = heapq.heappop(open_set)

        if iterations % 1000 == 0:
            print(f"Iteration {iterations}: open_set size {len(open_set)}, current path length {len(path)}")

        
        if len(path) >= max_depth:
            continue

        if path and current_state.scoreboard.score > best_score:
            best_score = current_state.scoreboard.score
            best_path = path
            print(f"New best score {best_score} at depth {len(path)}")

        key = state_key(current_state)
        if key in closed_set:
            continue
        closed_set.add(key)

        moves = possible_moves(current_state)

        for move in moves:
            new_state = apply_move(current_state, move, cakes)
            new_path = path + [move]
            new_cost = cost(new_state)
            new_priority = new_cost + heuristic(new_state, cakes, slice_count)
            heapq.heappush(open_set, (new_priority, next(counter), new_state, new_path))

    elapsed = time.time() - start_time
    print(f"A* finished after {iterations} iterations in {elapsed:.2f} seconds.")

    if not best_path:
        fallback_moves = possible_moves(initial_state)
        if fallback_moves:
            print("Returning fallback move.")
            return [fallback_moves[0]]
        else:
            print("No fallback move available.")
            return []
    return best_path


