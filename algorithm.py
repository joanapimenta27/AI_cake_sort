from collections import deque
import copy

from utils import *



def bfs_solver(initial_state, depth):
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
                new_state = apply_move(state, move)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, moves + [move]))
    

    return best_moves