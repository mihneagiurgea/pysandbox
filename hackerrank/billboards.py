from collections import deque


class QueueWithMin(object):

    def __init__(self):
        self.queue = deque()
        self.min_queue = deque()

    def enqueue(self, value):
        self.queue.append(value)
        while self.min_queue and self.min_queue[-1] > value:
            self.min_queue.pop()
        self.min_queue.append(value)

    def dequeue(self):
        value = self.queue.popleft()
        if value == self.min_queue[0]:
            self.min_queue.popleft()
        return value

    def top(self):
        if self.min_queue:
            return self.min_queue[0]
        else:
            return None


def read(f):
    N, K = map(int, f.readline().split())
    A = map(int, f.read().split())
    return (A, K)


def solve(A, K):
    """Dynamic programming:

    D[i] = minimum sum of choosing which billboards to remove from A[0..i],
           by removing billboard at position i
    Solution is D[N] (sentinel billboard with value 0).

    Recursion: D[i] = A[i] + min(D[j] | j = i-k-1..i-1)
    """
    min_queue = QueueWithMin()
    min_queue.enqueue(0)
    for i in xrange(len(A)):
        if i > K:
            min_queue.dequeue()
        d_i = A[i] + min_queue.top()
        min_queue.enqueue(d_i)
    if len(A) > K:
        min_queue.dequeue()
    return sum(A) - min_queue.top()

if __name__ == '__main__':
    import sys
    f = sys.stdin
    f = open(__file__.replace(".py", ".txt"))
    print solve(*read(f))
