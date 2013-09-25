from collections import defaultdict

class Node(object):

    def __init__(self, uid, value, left=None, right=None):
        self.uid = uid
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return '%s' % self.uid

class Path(object):

    def __init__(self, n1, n2, value):
        self.n1 = n1
        self.n2 = n2
        self.value = value

    def __repr__(self):
        return '%s -> %s (v: %d)' % (self.n1, self.n2, self.value)

def make_tree():
    n9 = Node(9, 9)
    two = Node(2, 2)
    four = Node(4, 4)
    five = Node(5, 5, None, n9)
    three = Node(3, 3, four, five)
    root = Node(1, 1, two, three)
    return root

class Solver(object):

    def __init__(self, root):
        self.root = root
        self.value_to_paths = defaultdict(list)
        self.total = 0

    def solve(self):
        self.find_paths(self.root)

    def find_paths(self, node):
        if node is None:
            return []

        paths_left = self.find_paths(node.left)
        paths_right = self.find_paths(node.right)
        paths = []
        for path in paths_left + paths_right:
            new_path = Path(path.n1, node, path.value + node.value)
            self.save_path(new_path)
            paths.append(new_path)

        new_path = Path(node, node, node.value)
        self.save_path(new_path)
        paths.append(new_path)

        for path_left in paths_left:
            for path_right in paths_right:
                new_path = Path(
                    path_left.n1,
                    path_right.n1,
                    path_left.value + path_right.value + node.value
                )
                self.save_path(new_path)

        return paths

    def save_path(self, path):
        self.value_to_paths[path.value].append(path)
        self.total += 1

def main():
    tree = make_tree()
    solver = Solver(tree)
    solver.solve()

    from pprint import pprint
    for value in sorted(solver.value_to_paths.keys()):
        print '\tValue: %d' % value
        pprint(solver.value_to_paths[value])
    print 'Total of %d paths' % solver.total

if __name__ == '__main__':
    main()