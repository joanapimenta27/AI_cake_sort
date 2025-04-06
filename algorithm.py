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


