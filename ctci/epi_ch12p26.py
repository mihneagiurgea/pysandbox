from collections import deque, namedtuple

Node = namedtuple('Node', ['v', 'c', 'l', 'r'])

def dfs(node, prefix, encoding):
    if node.c is not None:
        encoding[node.c] = prefix
    else:
        dfs(node.l, prefix + '0', encoding)
        dfs(node.r, prefix + '1', encoding)

def huffman(freqs):
    characters = []
    for char, freq in freqs.iteritems():
        node = Node(freq, char, None, None)
        characters.append(node)

    characters.sort(key=lambda node: node.v, reverse=True)

    q1 = deque(characters)
    q2 = deque()

    def min_dequeue(q1, q2):
        if q1 and q2:
            if q1[-1] < q2[-1]:
                return q1.pop()
            else:
                return q2.pop()
        else:
            if q1:
                return q1.pop()
            else:
                return q2.pop()

    while len(q1) + len(q2) > 1:
        right = min_dequeue(q1, q2)
        left = min_dequeue(q1, q2)
        # Make a new node, and push it into the 2nd queue.
        node = Node(left.v + right.v, None, left, right)
        q2.appendleft(node)

    root = q2.pop()

    encoding = {}
    dfs(root, '', encoding)

    return encoding

freqs = {'e': 12, 'a': 8, 'l': 4, 'm': 2.5, 'x': 0.15, 'z': 0.07}
print huffman(freqs)
