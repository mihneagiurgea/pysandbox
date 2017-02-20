import sys

from game_state import GameState
from strategies import BruteForceStrategy
from traversal import DFSWalk, Traversal


def main():
    string = sys.argv[1]
    print '=== Analyzing GameTree for %s ===' % string
    root = GameState.from_string(string)
    strategy = BruteForceStrategy()

    dfs_walk = DFSWalk(strategy)
    outcome = dfs_walk.walk(root)
    print 'Outcome of %s is %+d' % (root, outcome)
    print 'Iterated through %d nodes' % len(dfs_walk.visited)
    # Traversal.make_graph(root, strategy)

if __name__ == '__main__':
    main()