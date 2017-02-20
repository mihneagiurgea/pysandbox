import time

from game_state import GameState
from strategies import BruteForceStrategy
from traversal import DFSWalk

STATES = [
    '20/20 (0/0): 7/7 vs 3/3, 3/3, 3/3, 1/1',
    '20/20 (0/0): 10/10 vs 3/3, 3/3, 3/3, 3/3, 1/1'
    # '20/20 (0/0): 7/7 vs 3/3, 3/3, 3/3',
]

WINNABLE_STATES = [
    '20/20 (0/0): 10/10 vs 3/3',
    '20/20 (0/0): 10/10 vs 3/3, 3/3, 3/3, 3/3, 1/1'
]

def main():
    strategy = BruteForceStrategy()
    for state_string in STATES:
        game_state = GameState.from_string(state_string)
        N = 5
        start_time = time.time()
        for _ in range(N):
            dfs_walk = DFSWalk(strategy)
            outcome = dfs_walk.walk(game_state)
        duration = time.time() - start_time
        average_run = duration / N

        nodes = len(dfs_walk.visited)
        print 'Outcome of %s is %+d' % (game_state, outcome)
        # print '\nTotal duration: %.4fs' % duration
        print '\tAverage run: %.4fs' % average_run
        print '\tAverage of %.2f nodes/s (total of %d nodes)' % \
              (nodes * 1.0 / average_run, nodes)


if __name__ == '__main__':
    main()