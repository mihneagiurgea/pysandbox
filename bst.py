class Node(object):

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = None
        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self

    def __repr__(self):
        return '<Node(%s)>' % self.value

    def traverse_inorder1(self):
        """Traverse tree inorder with O(1) space using parent links."""
        prev = None
        node = self
        while node:
            # If prev node is parent or node is root:
            if (prev and prev == node.parent) or (not prev and node == self):
                # If we can, go left, otherwise continue traversing right
                # subtree.
                if node.left:
                    prev = node
                    node = node.left
                    continue
                else:
                    prev = node.left

            if prev == node.left:
                yield node

            if prev == node.left and node.right:
                # Go right
                prev = node
                node = node.right
            else:
                # Go up.
                prev = node
                node = node.parent


def is_bst(node, lower_bound=None, upper_bound=None):
    # node should be in (lower_bound, upper_bound)
    if lower_bound is not None and node.value <= lower_bound:
        return False
    if upper_bound is not None and node.value >= upper_bound:
        return False

    if node.left:
        if not is_bst(node.left, lower_bound, node.value):
            return False
    if node.right:
        if not is_bst(node.right, node.value, upper_bound):
            return False
    return True

def has_loop(node):
    """Determine if a linked list contains a loop, with O(1) space."""
    if node is None or node.tail is None:
        return False
    slow = node.tail
    fast = node.tail.tail
    while slow != fast and fast and fast.tail:
        slow = slow.tail
        fast = fast.tail.tail
    return slow == fast

def is_cdll(node):
    """Determine if node is a circular double linked list, in O(1) space."""
    # What if the list contains some other cycle?
    prev = node
    i = node.right
    while i is not None and i != node:
        if i.left != prev:
            return False
        prev = i
        i = i.right
    if i is None:
        return False
    if i.left != prev:
        return False
    return True

def copy_rplist(head):
    # Step 1 - for each node i, create its copy i' such that
    #   i -> i' -> i+1
    node = head
    while node:
        next = node.tail
        copy = Node(node.value)
        copy.tail = node.tail
        node.tail = copy
        node = next

    # Step 2 - copy random pointers
    node = head
    while node:
        if node.random is not None:
            node.tail.random = node.random.tail
        node = node.tail.tail

    # Step 3 - separate clones list into a different list.
    head_copy = head.tail
    node = head
    while node:
        node_copy = node.tail
        node.tail = node.tail.tail
        node_copy.tail = node_copy.tail.tail
        node = node.tail
    return head_copy



def bst_to_cdll(node):
    """Convert a BST to a circular double linked list."""

    def append(ll1, ll2):
        """Append 2 circular double linked lists together."""
        ll1.left.right = ll2
        ll2.left = ll1.left
        ll2.left.right = ll1
        ll1.left = ll2.left
        return ll1

    left_tree = node.left
    right_tree = node.right
    # Convert node into a circular dbl ll.
    node.left = node.right = node
    result = node
    if left_tree:
        left = bst_to_cdll(left_tree)
        result = append(left, result)
    if right_tree:
        right = bst_to_cdll(right_tree)
        result = append(result, right)
    return result



minf = float("-inf")
pinf = float("+inf")
root = Node(4,
    Node(2, Node(1), Node(3)),
    Node(5))
root = Node(-1, left=None, right=root)
root = Node(100, root, None)
print list(root.traverse_inorder1())
# print is_cdll(bst_to_cdll(root))
