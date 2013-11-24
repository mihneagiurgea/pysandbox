class Node(object):

    def __init__(self, children=None):
        self.children = children

def lcs(n1, n2):
    """Largest common subtree with root in n1 and n2."""
    return f(n1, n2, len(n1.children), len(n2.children))


def f(n1, n2, i, j):
    """Largest common subtree with root in n1 and n2, using only the first
    i children of n1 and first j children of n2.
    """
    if i == 0 or j == 0:
        return 1
    result = max(
        f(n1, n2, i-1, j),
        f(n1, n2, i, j-1),
        f(n1, n2, i-1, j-1) + lcs(n1.children[i-1], n2.children[j-1])
    )
    return result




