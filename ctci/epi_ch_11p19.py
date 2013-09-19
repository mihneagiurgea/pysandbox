"""
>>> tree = Node('__no_client__')
>>> tree.insert('mike', 1)
>>> tree.lookup('mike').value
1
>>> tree.max
1
>>> tree.insert('steve', 5)
>>> tree.max
5
>>> tree.insert('john', 7)
>>> tree.max
7
>>> tree.insert('alex', 6)
>>> tree.max
7
>>> tree.insert('luke', 12)
>>> tree.max
12
>>> tree.insert('laura', 17)
>>> tree.max
17
>>> tree.lookup('luke').value
12
>>> tree.addAll(2)
>>> tree.lookup('mike').value
3
>>> tree.lookup('john').value
9
>>> tree.lookup('luke').value
14
>>> tree.max
19
>>> tree.addAll(3)
>>> tree.insert('steve', 99)
>>> tree.lookup('steve').value
99
>>> tree.max
99
>>> tree.lookup('laura').value
22
>>> # Delete Case I
>>> tree.remove('steve')
>>> tree.max
22
>>> # Delete Case II
>>> tree.insert('luke', 47)
>>> tree.max
47
>>> tree.remove('luke')
>>> tree.max
22
>>> # Delete Case III
>>> tree.insert('john', 47)
>>> tree.max
47
>>> tree.remove('john')
>>> tree.max
22
"""


class Node(object):

    def __init__(self, client, value=0, left=None, right=None):
        self.key = client
        self.value = value
        self.left = left
        self.right = right
        self.add_all = 0
        self.max = 0
        self._update_max()

    def __str__(self):
        return '<Node(%s, %d, add_all=%d, max=%d)>' % \
               (self.key, self.value, self.add_all, self.max)

    def _push_down_add_all(self):
        if self.add_all:
            self.value += self.add_all
            if self.left:
                self.left.addAll(self.add_all)
            if self.right:
                self.right.addAll(self.add_all)
            self.add_all = 0

    def _update_max(self):
        self.max = self.value
        if self.left:
            self.max = max(self.max, self.left.max)
        if self.right:
            self.max = max(self.max, self.right.max)

    def addAll(self, value):
        self.add_all += value
        self.max += value

    def lookup(self, key):
        self._push_down_add_all()
        if self.key == key:
            return self
        elif self.key < key:
            return self.right.lookup(key)
        else:
            return self.left.lookup(key)

    def insert(self, key, value):
        self._push_down_add_all()
        if self.key == key:
            self.value = value
        elif self.key < key:
            if self.right is None:
                self.right = Node(key, value=value)
            else:
                self.right.insert(key, value)
        else:
            if self.left is None:
                self.left = Node(key, value=value)
            else:
                self.left.insert(key, value)
        self._update_max()

    def find_rightmost_node(self):
        node = self
        node._push_down_add_all()
        while node.right is not None:
            node = node.right
            node._push_down_add_all()
        return node

    def remove(self, key, parent=None):
        self._push_down_add_all()

        if self.key == key:
            self._delete(parent)
        elif self.key < key:
            self.right.remove(key, self)
        else:
            self.left.remove(key, self)

        # print 'Updating max for %s from %s and %s' % (self, self.left, self.right)
        self._update_max()

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
            predecessor = self.left.find_rightmost_node()
            self.value = predecessor.value
            self.left.remove(predecessor.key, self.left)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
