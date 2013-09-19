from collections import defaultdict, deque

class DirectedGraph(object):

    def __init__(self, N):
        self.N = N
        self.outgoing = defaultdict(list)
        self.incoming = defaultdict(list)

    def add_edge(self, i, j):
        self.outgoing[i].append(j)
        self.incoming[j].append(i)

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

    def topological_sort(self):
        current_in_degree = {}
        for i in range(1, self.N+1):
            current_in_degree[i] = len(self.incoming[i])

        result = []

        # A source is a vertex with in-degree = 0.
        sources = deque([i for i in range(1, self.N+1) if current_in_degree[i] == 0])
        while sources:
            node = sources.popleft()
            # Remove this node from graph, as well as all outgoing edges.
            for adjacent in self.outgoing[node]:
                current_in_degree[adjacent] -= 1
                if current_in_degree[adjacent] == 0:
                    sources.append(adjacent)
            result.append(node)

        if len(result) == self.N:
            return result
        else:
            raise ValueError('Digraph has cycles')

if __name__ == '__main__':
    digraph = DirectedGraph.from_file('digraph.in')
    print digraph.topological_sort()