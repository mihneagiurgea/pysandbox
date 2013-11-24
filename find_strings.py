# https://www.interviewstreet.com/challenges/dashboard/#problem/4efa210eb70ac
import sys
from collections import defaultdict

class FindStrings(object):

    def __init__(self, f):
        self.f = f
        self.read()
        self.generate_substrings()
        self.sort_substrings()
        self.remove_duplicates()

    def read(self):
        N = int(self.f.readline())

        self.V = []
        for i in xrange(N):
            S = self.f.readline().strip()
            self.V.append(S)

    def generate_substrings(self):
        self.substrings = []
        for k, S in enumerate(self.V):
            L = len(S)
            for i in xrange(0, L):
                for j in xrange(i+1, L+1):
                    t = (k, i, j)
                    self.substrings.append(t)

    def sort_substrings(self):
        """Sorts an array of strings; not in-place."""
        max_len = max( len(string) for string in self.V )

        result = range(len(self.substrings))
        buckets = defaultdict(list)
        for pos in xrange(max_len-1, -1, -1):
            for idx in result:
                k, i, j = self.substrings[idx]

                if pos < j - i:
                    char = self.V[k][i+pos]
                else:
                    char = 0
                buckets[char].append(idx)

            keys = buckets.keys()
            keys.sort()
            current = 0
            for key in keys:
                for idx in buckets.pop(key):
                   result[current] = idx
                   current += 1

        temp = [ self.substrings[i] for i in result ]
        self.substrings = temp

    def remove_duplicates(self):
        unique = [ ]
        last = None
        for substring in self.substrings:
            k, i, j = substring
            S = self.V[k][i:j]
            if S != last:
                unique.append(substring)
            last = S
        self.substrings = unique

    def answer_queries(self):
        Q = int(self.f.readline())
        for _ in xrange(Q):
            K = int(f.readline()) - 1
            if K < len(self.substrings):
                k, i, j = self.substrings[K]
                print self.V[k][i:j]
            else:
                print 'INVALID'

if __name__ == '__main__':
    f = sys.stdin
    f = open('find_strings.in')

    obj = FindStrings(f)
    obj.answer_queries()
