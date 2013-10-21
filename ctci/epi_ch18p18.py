class Matching(object):

    def __init__(self, N):
        self.N = N
        self.left = [None] * N
        self.right = [None] * N
        self._matched = 0

    def get_unmatched_left(self):
        for i in range(self.N):
            if self.left[i] is None:
                return i
        raise ValueError('All nodes are matched')

    def __len__(self):
        return self._matched

    def match(self, i, j):
        if self.left[i] is not None:
            self.unmatch_left(i)
        if self.right[j] is not None:
            self.unmatch_right(j)
        self.left[i] = j
        self.right[j] = i
        self._matched += 1

    def unmatch_left(self, i):
        j = self.left[i]
        if j is not None:
            self.left[i] = self.right[j] = None
            self._matched -= 1

    def unmatch_right(self, i):
        self.unmatch_left(self.right[i])


def find_stable_assignment(left_prefs, right_prefs):
    N = len(left_prefs)
    matching = Matching(N)
    while len(matching) < N:
        # Find an unmatched left node i.
        i = matching.get_unmatched_left()

        # Try to match i with some right node.
        for j in left_prefs[i]:
            # Get current match of j
            matched_j = matching.right[j]

            if matched_j is None:
                matching.match(i, j)
                break
            else:
                # If j prefers i to its current matching, match i with j.
                for k in right_prefs[j]:
                    if k == i or k == matched_j:
                        break
                if k == i:
                    matching.match(i, j)
                    break
    return matching

left_prefs = [
    [0, 1, 2],
    [1, 2, 0],
    [2, 1, 0]
]
right_prefs = [
    [0, 1, 2],
    [1, 2, 0],
    [2, 1, 0]
]

matching = find_stable_assignment(left_prefs, right_prefs)
print matching.left







