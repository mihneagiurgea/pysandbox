max_down = {}

def dfs(node):
    solution = -1
    costs = []
    for child, cost in node.children:
        solution = max(solution, dfs(child))
        costs.append(max_down[child] + cost)
    costs.sort(reverse=True)

    if len(costs) >= 1:
        max_down[node] = costs[0]
        solution = max(solution, costs[0])
    else:
        max_down[node] = 0
    if len(costs) >= 2:
        solution = max(solution, costs[0] + costs[1])
    return solution

class Node(object):

    def __init__(self, children=None):
        if children is None:
            self.children = []
        else:
            self.children = children

def main():
    node_d = Node([ (Node(), 1), (Node(), 2), (Node(), 3) ])
    node_h = Node()
    node_c = Node([ (node_h, 4), (node_d, 2) ])
    node_b = Node([ (node_c, 4), (Node(), 6) ])
    root = Node([ (Node(), 2), (node_b, 1) ])
    print dfs(root)

main()

