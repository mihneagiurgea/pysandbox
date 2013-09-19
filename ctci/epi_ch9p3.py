class Node(object):

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self._hash_value = None

    def _get_hash(self):
        M = 666013
        B = 1024
        hash_left = 0 if self.left is None else self.left.hash
        hash_right = 0 if self.right is None else self.right.hash
        return (self.value * B * B + hash_left * B + hash_right) % M

    @property
    def hash(self):
        if self._hash_value is None:
            self._hash_value = self._get_hash()
        return self._hash_value

    def __repr__(self):
        if self.left is None and self.right is None:
            return 'Node(%d)' % self.value
        else:
            return 'Node(%d, %r, %r)' % (self.value, self.left, self.right)


def df(node, hash_to_node):
    if node.left is not None:
        node.left = df(node.left, hash_to_node)
    if node.right is not None:
        node.right = df(node.right, hash_to_node)
    if node.hash not in hash_to_node:
        hash_to_node[node.hash] = node
    return hash_to_node[node.hash]


def solve(trees):
    transformed_trees = []
    hash_to_node = {}
    for tree in trees:
        transformed_trees.append(df(tree, hash_to_node))
    return transformed_trees

if __name__ == '__main__':
    tree_1 = Node(
        3,
        Node(
            2,
            Node(1, Node(0))
        )
    )
    tree_2 = Node(
        9,
        Node(5, Node(3), Node(7)),
        Node(11)
    )
    tree_3 = Node(
        2,
        Node(1, Node(0)),
        Node(5, Node(3), Node(7))
    )
    trees = [tree_1, tree_2, tree_3]
    transformed_trees = solve(trees)
    print transformed_trees
