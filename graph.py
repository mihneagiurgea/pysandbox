from collections import defaultdict

class DFSResult(object):

    def __init__(self, graph):
        self.graph = graph
        self.node_to_parent = {}
        self.node_to_level = {}
        self.critical_edges = []

    def dfs(self, node, level=1):
        min_level = self.node_to_level[node] = level
        for i in self.graph.neighbours[node]:
            if i not in self.node_to_level:
                # Node "i" was not yet visited.
                self.node_to_parent[i] = node
                min_level_i = self.dfs(i, level+1)

                # Is the edge (node -> i) a critical one?
                if min_level_i == level + 1:
                    self.critical_edges.append((node, i))

                min_level = min(min_level, min_level_i)

            elif self.node_to_level[i] == level - 1:
                # Node "i" is parent of current node, don't do anything.
                pass
            else:
                # node -> i is a back edge.
                min_level = min(min_level, self.node_to_level[i])

        return min_level


class UndirectedGraph(object):

    def __init__(self, N):
        self.N = N
        self.neighbours = defaultdict(list)

    def add_edge(self, i, j):
        self.neighbours[i].append(j)
        self.neighbours[j].append(i)

    @classmethod
    def from_file(cls, filename):
        f = open(filename, 'r')
        N, M = map(int, f.readline().split())
        graph = cls(N)
        for _ in range(M):
            i, j = map(int, f.readline().split())
            graph.add_edge(i, j)
        f.close()
        return graph

    def get_critical_edges(self):
        dfs_result = DFSResult(self)
        dfs_result.dfs(1)
        return dfs_result.critical_edges

if __name__ == '__main__':
    graph = UndirectedGraph.from_file('graph.in')
    print graph.get_critical_edges()
