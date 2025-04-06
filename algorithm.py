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

    nodes_visited = 0

    while queue:
        nodes_visited += 1
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
    

    return best_moves, nodes_visited



def dfs_solver(initial_state, depth, cakes):
    visited = set()
    stack = []
    stack.append((initial_state, []))
    visited.add(initial_state)

    best_moves = []
    best_score = -float('inf')

    nodes_visited = 0

    while stack:
        nodes_visited += 1
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

    return best_moves, nodes_visited


def monte_carlo_solver(initial_state, iterations, depth, cakes):

    best_moves = []
    best_score = -float('inf')

    nodes_visited = 0

    for _ in range(iterations):
        simulation_state = initial_state.copy()
        moves_sim = []
        for _ in range(depth):
            moves = possible_moves(simulation_state)
            if not moves:
                break
            move = random.choice(moves)
            simulation_state = apply_move(simulation_state, move, cakes)
            moves_sim.append(move)
            nodes_visited += 1

        score = simulation_state.scoreboard.score
        if score > best_score:
            best_score = score
            best_moves = moves_sim
    return best_moves, nodes_visited


def hint_solver(initial_state, algorithm, cakes):
    if algorithm == 'BFS':
        return bfs_solver(initial_state, 2, cakes)[0]
    elif algorithm == 'DFS':
        return dfs_solver(initial_state, 2, cakes)[0]
    elif algorithm == 'greedy':
        #return greedy_solver(initial_state, cakes)
        pass
    elif algorithm == 'a_star':
        #return a_star_solver(initial_state, cakes)
        pass
    elif algorithm == 'Monte Carlo':
        return monte_carlo_solver(initial_state, 100, 15, cakes)[0]
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    

