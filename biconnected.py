from collections import defaultdict
from graph import UndirectedGraph


class BiconnectedComponents(object):

    def __init__(self, graph):
        self.graph = graph
        self.depth = {}
        self.low = {}
        self.articulations = set()
        self.bridges = []
        self.bcc = {}
        self._current_bcc = 0
        self._edge_stack = []

    def compute(self, root=1):
        self._current_bcc = 0
        self.dfs(root, 1)

        # Pop the remainder of the stack.
        self._current_bcc += 1
        while self._edge_stack:
            self.bcc[self._edge_stack.pop()] = self._current_bcc

        # Is the root an articulation point?
        if root in self.articulations:
            self.articulations.remove(root)
        root_children = self.depth.values().count(self.depth[root] + 1)
        if root_children >= 2:
            self.articulations.add(root)

        print 'Articulations: %s' % sorted(list(self.articulations))
        print 'Bridges: %s' % sorted(self.bridges)

        bcc_to_edge = defaultdict(list)
        for edge, bcc in self.bcc.iteritems():
            bcc_to_edge[bcc].append(edge)

        print 'Biconnected components:'
        for bcc in bcc_to_edge:
            print '#%d: %s' % (bcc, bcc_to_edge[bcc])

    def dfs(self, node, current_depth=1):
        self.depth[node] = current_depth

        self.low[node] = current_depth
        for child in self.graph.neighbours[node]:
            if child not in self.depth:
                # (node -> child) is a forward edge
                self.dfs(child, current_depth + 1)
                self.low[node] = min(self.low[node], self.low[child])
                self._edge_stack.append((node, child))

                if self.low[child] >= current_depth:
                    self.articulations.add(node)

                    # Each articulation point closes a biconnected component.
                    self._current_bcc += 1
                    while self._edge_stack:
                        i, j = self._edge_stack[-1]
                        if max(self.depth[i], self.depth[j]) > current_depth:
                            self.bcc[self._edge_stack.pop()] = self._current_bcc
                        else:
                            break

                if self.low[child] > current_depth:
                    self.bridges.append((node, child))

            elif self.depth[child] < current_depth - 1:
                # (node -> child) is a back edge, update low[node]
                self.low[node] = min(self.low[node], self.depth[child])
                self._edge_stack.append((node, child))


if __name__ == '__main__':
    graph = UndirectedGraph.from_file('graph.in')
    bc = BiconnectedComponents(graph)
    bc.compute()