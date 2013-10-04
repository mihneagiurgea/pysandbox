class RandomListNode(object):

    def __init__(self, label, next=None, random=None):
        self.label = label
        self.next = next
        self.random = random

    def __getitem__(self, key):
        if key == 0:
            return self
        else:
            return self.next[key-1]

    def __str__(self):
        random_label = self.random.label if self.random else None
        return '(%r, ~~>%r)' % (self.label, random_label)

    def __repr__(self):
        if self.next:
            return '%s --> %r' % (self, self.next)
        else:
            return '%s -/->' % self

    def deepcopy(self):
        # Step 1 - copy each node and insert it between the original node
        # and the next one.
        node = self
        while node:
            node_copy = RandomListNode(node.label, node.next)
            node.next = node_copy
            node = node_copy.next

        # Step 2 - set random pointers into all copied nodes.
        node = self
        while node:
            if node.random:
                node.next.random = node.random.next

            node = node.next.next

        # Step 3 - fix next pointers in original list and copied list.
        head_copy = self.next
        node = self
        while node:
            node_copy = node.next
            # Fix original node next pointer.
            node.next = node_copy.next
            if node_copy.next:
                node_copy.next = node_copy.next.next

            node = node.next

        return head_copy

def make_list(n, label=1):
    if n == 0:
        return None
    else:
        return RandomListNode(label, make_list(n-1, label+1))

ls = make_list(4)
ls[0].random = ls[3]
ls[1].random = ls[2]
ls[2].random = ls[0]
ls[3].random = ls[1]
print 'ls: %r' % ls
print 'ls[2]: %s' % ls[2]

ls_copy = ls.deepcopy()
print 'ls: %r' % ls
print 'ls_copy: %r' % ls_copy