from collections import deque
import copy
import random

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


