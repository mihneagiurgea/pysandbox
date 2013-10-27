# Implemented all problems from here in a Python way:
# http://cslibrary.stanford.edu/105/LinkedListProblems.pdf

class LinkedListNode(object):

    def __init__(self, value, tail=None):
        self.value = value
        self.tail = tail

    def __repr__(self):
        if self.tail is None:
            return '%r-/->' % self.value
        else:
            return '%r-->%r' % (self.value, self.tail)

class LinkedList(object):

    def __init__(self, *args):
        """
        >>> LinkedList(1, 2, 3)
        1-->2-->3-/->
        >>> LinkedList(1)
        1-/->
        >>> LinkedList()
        -/->
        """
        if len(args) == 0:
            self.head = None
        else:
            self.head = LinkedListNode(args[0])
            last = self.head
            for i in range(1, len(args)):
                last.tail = LinkedListNode(args[i])
                last = last.tail

    def __repr__(self):
        if self.head is None:
            return '-/->'
        else:
            return repr(self.head)

    def count(self, value):
        """Return number of occurrences of value.

        >>> ls = LinkedList(1, 2, 2, 4, 5)
        >>> ls.count(2)
        2
        >>> ls.count(3)
        0
        """
        node = self.head
        count = 0
        while node is not None:
            if node.value == value:
                count += 1
            node = node.tail
        return count

    def __getitem__(self, key):
        """
        >>> ls = LinkedList(1, 2, 2, 4, 5)
        >>> ls[0]
        1
        >>> ls[4]
        5
        """
        node = self.head
        while key > 0:
            node = node.tail
            key -= 1
        return node.value

    def pop(self):
        """
        >>> ls = LinkedList(1, 2, 3, 4)
        >>> ls.pop()
        1
        >>> ls.pop()
        2
        """
        if self.head is None:
            raise IndexError('pop from empty linked list')
        value = self.head.value
        next_head = self.head.tail
        del self.head
        self.head = next_head
        return value

    def push(self, value):
        """
        >>> ls = LinkedList()
        >>> ls.push(1)
        >>> ls
        1-/->
        >>> ls.push(2)
        >>> ls
        2-->1-/->
        """
        self.insert(0, value)

    def delete_list(self):
        """
        >>> ls = LinkedList(*range(4))
        >>> ls.delete_list()
        """
        node = self.head
        while node is not None:
            next = node.tail
            node.tail = None
            del node
            node = next

    def insert(self, index, value):
        """Insert value before index.

        >>> ls = LinkedList()
        >>> ls.insert(0, 5)
        >>> ls.insert(0, 4)
        >>> ls
        4-->5-/->
        >>> ls.insert(1, 3)
        >>> ls
        4-->3-->5-/->
        >>> ls.insert(3, 2)
        >>> ls
        4-->3-->5-->2-/->
        """
        new_node = LinkedListNode(value)
        if index == 0:
            new_node.tail = self.head
            self.head = new_node
        else:
            node = self.head
            while index > 1:
                node = node.tail
                index -= 1
            new_node.tail = node.tail
            node.tail = new_node

    def sorted_insert(self, node):
        """Inserts node in a list that is sorted in increasing order, such
        that the order is maintained.
        >>> ls = LinkedList()
        >>> ls.sorted_insert(LinkedListNode(3))
        >>> ls
        3-/->
        >>> ls.sorted_insert(LinkedListNode(5))
        >>> ls.sorted_insert(LinkedListNode(1))
        >>> ls
        1-->3-->5-/->
        >>> ls.sorted_insert(LinkedListNode(2))
        >>> ls
        1-->2-->3-->5-/->
        >>> ls.sorted_insert(LinkedListNode(0))
        >>> ls
        0-->1-->2-->3-->5-/->
        >>> ls.sorted_insert(LinkedListNode(6))
        >>> ls
        0-->1-->2-->3-->5-->6-/->
        """
        if self.head is None:
            self.head = node
            self.head.tail = None
        elif node.value < self.head.value:
            node.tail = self.head
            self.head = node
        else:
            insert_after = self.head
            while insert_after.tail and insert_after.tail.value < node.value:
                insert_after = insert_after.tail
            node.tail = insert_after.tail
            insert_after.tail = node

    def insert_sort(self):
        """Sort in place using self.sorted_insert.

        >>> ls = LinkedList(7, 1, 6, 4, 5, 2, 3)
        >>> ls.insert_sort()
        >>> ls
        1-->2-->3-->4-->5-->6-->7-/->
        """
        sorted_list = LinkedList()
        while self.head is not None:
            node = self.head
            self.head = self.head.tail
            sorted_list.sorted_insert(node)
        self.head = sorted_list.head

    def append(self, ll):
        """Append another LinkedList to this one.
        >>> a = LinkedList()
        >>> b = LinkedList(1, 2)
        >>> a.append(b)
        >>> a
        1-->2-/->
        >>> b
        -/->
        >>> c = LinkedList(3, 4)
        >>> a.append(c)
        >>> a
        1-->2-->3-->4-/->
        >>> c
        -/->
        """
        if self.head is None:
            self.head = ll.head
        else:
            node = self.head
            while node.tail:
                node = node.tail
            node.tail = ll.head
        ll.head = None

    def front_back_split(self):
        """
        >>> ls = LinkedList(1)
        >>> ls.front_back_split()
        (1-/->, -/->)
        >>> ls = LinkedList(1, 2)
        >>> ls.front_back_split()
        (1-/->, 2-/->)
        >>> ls = LinkedList(1, 2, 3)
        >>> ls.front_back_split()
        (1-->2-/->, 3-/->)
        >>> ls = LinkedList(1, 2, 3, 4)
        >>> ls.front_back_split()
        (1-->2-/->, 3-->4-/->)
        >>> ls
        1-->2-/->
        """
        if self.head is None:
            return self, LinkedList()

        fast = slow = self.head
        while fast.tail and fast.tail.tail:
            slow = slow.tail
            fast = fast.tail.tail
        back_list = LinkedList()
        back_list.head = slow.tail
        slow.tail = None
        return self, back_list

    def remove_duplicates(self):
        """
        >>> ls = LinkedList(1, 2, 2, 2, 3, 3, 4)
        >>> ls.remove_duplicates()
        >>> ls
        1-->2-->3-->4-/->
        >>> ls = LinkedList(1, 1, 2, 2, 2, 3, 3, 4)
        >>> ls.remove_duplicates()
        >>> ls
        1-->2-->3-->4-/->
        """
        prev_node = self.head
        node = self.head.tail
        while node:
            if node.value == prev_node.value:
                prev_node.tail = node.tail
            else:
                prev_node = node
            node = node.tail

    def move_node(self, ll):
        """
        >>> a = LinkedList(1, 2, 3)
        >>> b = LinkedList(1, 2, 3)
        >>> a.move_node(b)
        >>> a
        1-->1-->2-->3-/->
        >>> b
        2-->3-/->
        """
        self.push(ll.pop())

    def reverse(self):
        """
        >>> LinkedList(1).reverse()
        1-/->
        >>> LinkedList(1, 2, 3).reverse()
        3-->2-->1-/->
        """
        if self.head is None:
            return self
        prev = self.head
        node = self.head.tail
        self.head.tail = None
        while node:
            # prev -> node -> node.tail
            node_tail = node.tail
            node.tail = prev
            prev = node
            node = node_tail
        self.head = prev
        return self

    def alternating_split(self):
        """
        >>> ls = LinkedList(1, 2, 1, 2, 1)
        >>> ls.alternating_split()
        (1-->1-->1-/->, 2-->2-/->)
        """
        first = LinkedList()
        second = LinkedList()
        while self.head:
            first.move_node(self)
            if self.head:
                second.move_node(self)
        return (first, second)

    def shuffle_merge(self, ll):
        """
        >>> a = LinkedList(1, 2, 3, 4, 5)
        >>> b = LinkedList(10, 11, 12)
        >>> a.shuffle_merge(b)
        1-->10-->2-->11-->3-->12-->4-->5-/->
        >>> a = LinkedList(1, 2, 3)
        >>> b = LinkedList(10, 11, 12, 13, 14)
        >>> a.shuffle_merge(b)
        1-->10-->2-->11-->3-->12-->13-->14-/->
        >>> b
        -/->
        """
        # What if self is empty?
        i = self.head
        j = ll.head
        ll.head = None
        while i and j:
            i_tail = i.tail
            j_tail = j.tail
            # i -> j -> i.tail ...
            i.tail = j
            if i_tail:
                j.tail = i_tail
            i = i_tail
            j = j_tail
        return self

    @classmethod
    def sorted_merge(cls, a, b):
        """
        >>> LinkedList.sorted_merge(LinkedList(2, 4), LinkedList(1, 3, 5))
        1-->2-->3-->4-->5-/->
        >>> LinkedList.sorted_merge(LinkedList(1, 3, 5), LinkedList(2, 4))
        1-->2-->3-->4-->5-/->
        >>> LinkedList.sorted_merge(LinkedList(1, 3, 5), LinkedList())
        1-->3-->5-/->
        >>> LinkedList.sorted_merge(LinkedList(), LinkedList(1, 3, 5))
        1-->3-->5-/->
        """
        result = LinkedList()
        while a.head and b.head:
            if a.head.value < b.head.value:
                result.move_node(a)
            else:
                result.move_node(b)
        while a.head:
            result.move_node(a)
        while b.head:
            result.move_node(b)
        return result.reverse()

    def merge_sort(self):
        """
        >>> ls = LinkedList(7, 1, 6, 5, 2, 3, 4)
        >>> ls.merge_sort()
        >>> ls
        1-->2-->3-->4-->5-->6-->7-/->
        """
        if self.head.tail is None:
            return
        front, back = self.front_back_split()
        front.merge_sort()
        back.merge_sort()
        self.head = LinkedList.sorted_merge(front, back).head




if __name__ == '__main__':
    import doctest
    doctest.testmod()