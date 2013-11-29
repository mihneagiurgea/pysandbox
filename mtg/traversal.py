from collections import deque

from constants import Outcome
from graph import DirectedGraph


class DFSWalk(object):

    def __init__(self, strategy):
        self.visited = set()
        self.node_to_outcome = {}
        self.strategy = strategy

    def walk(self, node):
        self.visited.add(node)

        if node.is_over:
            # print 'Found terminal node: %s' % node
            self.node_to_outcome[node] = node.outcome
            return node.outcome

        outcome = Outcome.Loss
        for next in self.strategy.get_next_states(node):
            if next in self.visited:
                if next in self.node_to_outcome:
                    # We have already computed this node => it is not an
                    # ancestor of this node => there is no cycle between
                    # node and next.
                    outcome_next = self.node_to_outcome[next]
                else:
                    # There is a cycle between node and next.
                    # Cycles give each player the possibility of drawing.
                    # If any of the two players has a better outcome (Win),
                    # then neither will be able to draw.
                    outcome_next = Outcome.Draw
            else:
                outcome_next = self.walk(next)

            if next.next_to_act != node.next_to_act:
                # Reverse outcome_next (win <-> loss).
                outcome_next = -outcome_next
            outcome = max(outcome, outcome_next)

            if outcome is Outcome.Win:
                # Found a winning move
                break
        # print 'Outcome( %s ) = %+d' % (node, outcome)
        self.node_to_outcome[node] = outcome

        return outcome


class Traversal(object):
    """Factory for creating the implied graph of game states, starting from
    some game state and some strategy."""

    @classmethod
    def get_outcome(cls, state, strategy):
        """Returns the outcome of the given state, by doing a complete DFS
        walk."""
        pass

    @classmethod
    def make_graph(cls, root, strategy):
        """Compute the graph implied by some GameState."""
        graph = DirectedGraph()

        queue = deque()
        visited = set()

        # Add root to queue
        visited.add(root)
        queue.append(root)

        while queue:
            node = queue.popleft()
            if not node.is_over:
                for next in strategy.get_next_states(node):
                    graph.add_arc(node, next)
                    if next not in visited:
                        # Add `next` to queue.
                        visited.add(next)
                        queue.append(next)

        return graph
