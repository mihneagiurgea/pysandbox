from collections import defaultdict


class DirectedGraph(object):
    """Used to represent an in-memory directed graph."""

    def __init__(self):
        self._node_to_neighbours = defaultdict(list)
        # For easier printing of this Graph, convert nodes to a sequence
        # of increasing integers.
        self._uid_to_node = {}
        self._node_to_uid = {}
        self._next_uid = 1

    def _to_int(self, node):
        if node not in self._node_to_uid:
            self._node_to_uid[node] = self._next_uid
            self._next_uid += 1
        return self._node_to_uid[node]

    def add_arc(self, x, y):
        """Add an x -> y arc."""
        self._node_to_neighbours[x].append(y)
        print '%r (%s) -> %r (%s)' % (self._to_int(x), x, self._to_int(y), y)