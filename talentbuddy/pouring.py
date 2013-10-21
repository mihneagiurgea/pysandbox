from collections import deque

class Pouring(object):

    def __init__(self, l, CA, CB):
        self.l = l
        self.CA = CA
        self.CB = CB

    def is_terminal(self, node):
        x, y = node
        return x == self.l or y == self.l

    def get_adjacent(self, node):
        x, y = node

        results = []
        results.append(((self.CA, y), 'fill A'))
        results.append(((x, self.CB), 'fill B'))

        results.append(((0, y), 'empty A'))
        results.append(((x, 0), 'empty B'))

        q = min(self.CB - y, x)
        state = (x - q, y + q)
        results.append((state, 'pour A into B'))

        q = min(self.CA - x, y)
        state = (x + q, y - q)
        results.append((state, 'pour B into A'))

        return results

def bfs(source, get_adjacent):
    q = deque()
    node_to_level = {}
    node_to_parent = {}

    q.append(source)
    node_to_level[source] = 1

    while q:
        node = q.popleft()
        for adj, label in get_adjacent(node):
            if adj not in node_to_level:
                q.append(adj)
                node_to_level[adj] = node_to_level[node] + 1
                node_to_parent[adj] = (node, label)

    return node_to_parent, node_to_level

def recover_path(node, node_to_parent):
    path = []
    while node in node_to_parent:
        parent, label = node_to_parent[node]
        path.append(label)
        node = parent
    path.reverse()
    return path

def pour_water(l, ca, cb):
    pouring = Pouring(l, ca, cb)

    source = (0, 0)
    node_to_parent, node_to_level = bfs(source, pouring.get_adjacent)

    closest_node = None
    for node in node_to_level:
        if pouring.is_terminal(node):
            if closest_node is None or node_to_level[node] < node_to_level[closest_node]:
                closest_node = node

    if closest_node is None:
        print 'impossible'
    else:
        path = recover_path(closest_node, node_to_parent)
        print '\n'.join(path)

pour_water(1, 5, 3)
