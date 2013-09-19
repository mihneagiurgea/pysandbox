class BSTNode(object):

    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        if self.value is None:
            return '<BSTNode(%s)>' % (self.key, )
        else:
            return '<BSTNode(%s -> %s)>' % (self.key, self.value)

    def create_node(self, key, value):
        # Create a new node instance with respect to inheritance
        # (do not hardcode the class name).
        return self.__class__(key, value)

    def find(self, key):
        if self.key == key:
            return self
        elif key < self.key:
            return self.left.lookup(key)
        else:
            return self.right.lookup(key)

    def insert(self, key, value):
        if self.key == key:
            self.value = value
        elif key < self.key:
            if self.left is None:
                self.left = self.create_node(key, value)
            else:
                self.left.insert(key, value)
        else:
            if self.right is None:
                self.right = self.create_node(key, value)
            else:
                self.right.insert(key, value)

    def find_rightmost(self):
        node = self
        while node.right is not None:
            node = node.right
        return node

    def remove(self, key, parent=None):
        print 'remove(%r) on %s(%s, %s)' % (key, self, self.left, self.right)
        if self.key == key:
            self._delete(parent)
        elif key < self.key:
            self.left.remove(key, self)
        else:
            self.right.remove(key, self)

    def _delete(self, parent):
        if self.left is None and self.right is None:
            # Case I - node is a terminal leaf
            if parent.left == self:
                parent.left = None
            else:
                parent.right = None
        elif self.left is None or self.right is None:
            # Case II - node has a single child
            child = self.left if self.left is not None else self.right
            if parent.left == self:
                parent.left = child
            else:
                parent.right = child
        else:
            # Case III - node has 2 children
            predecessor = self.left.find_rightmost()
            self.key = predecessor.key
            self.value = predecessor.value
            self.left.remove(predecessor.key, self.left)


class IntervalTreeNode(BSTNode):

    def __init__(self, x, y):
        BSTNode.__init__(self, (x, y), None)
        self._update_y_max()

    @property
    def x(self):
        return self.key[0]

    @property
    def y(self):
        return self.key[1]

    def __str__(self):
        return '<IntervalTreeNode([%d, %d], y_max=%d)>' % (self.x, self.y, self.y_max)

    def _update_y_max(self):
        self.y_max = self.y
        if self.left:
            self.y_max = max(self.y_max, self.left.y_max)
        if self.right:
            self.y_max = max(self.y_max, self.right.y_max)

    def insert(self, key, value):
        BSTNode.insert(self, key, value)
        self._update_y_max()

    def remove(self, key, parent=None):
        BSTNode.remove(self, key, parent)
        self._update_y_max()

    def lookup(self, L, R):
        """Return an interval that intersects [L, R], or None, if no such
        interval exists."""
        if L <= self.x <= R or self.x <= L <= self.y:
            # This node's interval intersects [L, R].
            return self
        elif self.left and self.left.y_max >= L:
            return self.left.lookup(L, R)
        elif self.right:
            return self.right.lookup(L, R)
        else:
            return None


if __name__ == '__main__':
    tree = IntervalTreeNode(10, 12)
    tree.insert(5, 8)
    tree.insert(6, 12)
    tree.insert(15, 18)
    tree.insert(19, 24)

    print tree.lookup(16, 17)
    # tree.remove((16, 17))

