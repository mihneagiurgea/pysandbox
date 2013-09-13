class Node(object):

    def __init__(self, value, left=None, right=None, next=None):
        self.value = value
        self.left = left
        self.right = right
        self.next = next

    def __str__(self):
        return '<Node(%d)>' % (self.value, )

    @property
    def first_child(self):
        return self.left if self.left else self.right

    def print_tree(self):
        leftmost = None
        node = self
        while node:
            if leftmost is None:
                if node.left or node.right:
                    leftmost = node.left if node.left else node.right
            print '%d -> ' % node.value,
            node = node.next
        print
        if leftmost:
            leftmost.print_tree()

def populate(node):

    def iter_children(node):
        while node:
            if node.left:
                yield node.left
            if node.right:
                yield node.right
            node = node.next

    while node:
        next_level = None
        last_child = None

        for child in iter_children(node):
            if next_level is None:
                next_level = child
            if last_child is not None:
                last_child.next = child
            last_child = child

        node = next_level


def main():
    # /*          1
    #  *        /   \
    #  *      2       3
    #  *     / \     / \
    #  *    4           7
    #  *   / \         / \
    #  *      9       14
    #  *
    #  */
    node4 = Node(4, None, Node(9))
    node7 = Node(7, Node(14), None)
    node2 = Node(2, node4, None)
    node3 = Node(3, None, node7)
    root = Node(1, node2, node3)

    populate(root)
    root.print_tree()

main()