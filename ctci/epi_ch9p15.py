# Sonia's solution with lists.
from collections import deque

def build_lists(S, Q):
    elem_to_index = {}
    for idx, q in enumerate(Q):
        elem_to_index[q] = idx

    positions_list = []
    for _ in range(len(Q)):
        positions_list.append(deque())

    for idx, s in enumerate(S):
        if s in elem_to_index:
            i = elem_to_index[s]
            positions_list[i].append(idx)
    return positions_list

def solve(S, Q):
    positions_list = build_lists(S, Q)

    best_solution = None
    best_solution_length = 0

    # The current solution is an array of indices into positions_list.
    current_solution = [0] * len(Q)
    current_solution[0] = -1

    while current_solution[0] < len(positions_list[0]):
        current_solution[0] += 1
        i = 1
        while i < len(Q) and positions_list[current_solution]
        for i in range(1, len(Q)):
            if





if __name__ == '__main__':
    Q = [1, 2, 3]
    S = [1, 2, 1, 0, 0, 0, 3, 1, 2, 3, 1, 1, 1, 2, 1, 0, 3, 1, 3]
    print solve(S, Q)