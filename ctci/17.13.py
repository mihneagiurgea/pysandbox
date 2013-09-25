class Node(object):

    def __init__(self, value, node1=None, node2=None):
        self.value = value
        self.left = node1
        self.right = node2

    def __str__(self):
        return '%r' % self.value

    def __repr__(self):
        pieces = []
        if self.left:
            pieces.append(repr(self.left))
        pieces.append(repr(self.value))
        if self.right:
            pieces.append(repr(self.right))
        return '<%s>' % ', '.join(pieces)

    def to_dll_string(self):
        head = self
        while head.left:
            head = head.left
        pieces = []
        while head is not None:
            pieces.append(str(head.value))
            if head.right:
                if head.right.left == head:
                    pieces.append('<->')
                else:
                    pieces.append('->')
            head = head.right
        return ''.join(pieces)

    def get_predecessor(self):
        predecessor = self.left
        while predecessor.right and predecessor.right != self:
            predecessor = predecessor.right
        return predecessor

    def get_successor(self):
        successor = self.right
        while successor.left and successor.left != self:
            successor = successor.left
        return successor

    def convert_to_dll(self):
        if self.left:
            self.left.convert_to_dll()
            predecessor = self.get_predecessor()
            predecessor.right = self
            self.left = predecessor
        if self.right:
            self.right.convert_to_dll()
            successor = self.get_successor()
            successor.left = self
            self.right = successor

    def bad(self):

        """Convert a BST to a sorted doubly linked list, in place."""
        if self.right and self.right.left == self:
            return
        print self

        if self.left:
            predecessor = self.left
            while predecessor.right and predecessor.right != self:
                predecessor = predecessor.right

            if predecessor.right != self:
                # Haven't covered the left subtree, do that now.
                predecessor.right = self
                self.left.convert_to_dll()
                return
            else:
                # Already covered the left subtree.
                self.left = predecessor
                # predecessor.right = None

        # Go right.
        print self.value
        if self.right:
            successor = self.right
            while successor.left and successor.left != self:
                successor = successor.left

            print 'Found successor for %s: %s' % (self, successor.value)
            if successor.left != self:
                # Haven't covered the right subtree, do that now.
                next = self.right
                self.right = successor
                successor.left = self

                next.convert_to_dll()


def main():
    six = Node(6,
               Node(5, Node(4)),
               Node(7))
    root = Node(3,
                Node(1, None, Node(2)),
                six)
    print root.to_dll_string()
    root.convert_to_dll()
    print root.to_dll_string()

if __name__ == '__main__':
    main()
