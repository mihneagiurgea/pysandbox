# https://www.interviewstreet.com/challenges/dashboard/#problem/4edb8abd7cacd
import sys
import array

class StringSimilarity(object):

    def __init__(self, S):
        self.S = self.string = S

    def count_sort(self, offset=0):
        K = max([self.key[a+offset] for a in self.ordered_suffixes]) + 1
        count = [0] * K
        for a in self.ordered_suffixes:
            count[self.key[a+offset]] += 1
        total = 0
        for i in xrange(K):
            c = count[i]
            count[i] = total
            total += c

        # temp := ordered_suffixes
        temp = [a for a in self.ordered_suffixes]

        for a in temp:
            pos = count[self.key[a+offset]]
            count[self.key[a+offset]] += 1
            self.ordered_suffixes[pos] = a

    def compute_suffix_arrays(self):
        N = len(self.string)

        # Each suffix is identified by its starting position in the initial string.
        self.ordered_suffixes = range(N)

        # Initially, sort each suffix using the 1st character; do this by
        # assigning a value to each suffix = ord(1st character).
        self.key = [ord(char) for char in self.string]
        # Extend the key array with N "0"-s, for easier suffix comparison.
        self.key.extend([0] * N)

        temp = [0] * N

        step = 1
        while step <= N:
            # Re-sort the suffixes, looking at the first 2*step characters;
            # the new key for each suffix becomes (key[i], key[i+step]), so
            # we'll just use a 2-step radix-sort.
            self.count_sort(offset=step)
            self.count_sort(offset=0)

            # Compute the new key (in a separate array).
            # The value of the smalles suffix is 1.
            temp[self.ordered_suffixes[0]] = last = 1
            for i in xrange(1, N):
                crnt = self.ordered_suffixes[i]
                prev = self.ordered_suffixes[i-1]
                # The value of the next smallest suffix is equal to
                # the last value +1 or +0.
                if (self.key[crnt] > self.key[prev] or
                    self.key[crnt+step] > self.key[prev+step]):
                    last += 1
                temp[self.ordered_suffixes[i]] = last
            # key := temp
            for i in xrange(N):
                self.key[i] = temp[i]

            step *= 2

        return self.ordered_suffixes

    def binsearch(self, suffixes, offset, x, lo, hi):
        # Invariant: A[lo] < x <= A[hi]
        while hi - lo > 1:
            mid = (lo + hi) / 2
            i = suffixes[mid] + offset
            char = self.S[i] if i < len(self.S) else '\0'
            if char < x:
                lo = mid
            else:
                hi = mid
        return hi

    def solve(self):
        suffixes = self.compute_suffix_arrays()

        result = 0

        lo = -1
        hi = len(self.string)
        for offset, char in enumerate(self.S):
            # Char + 1 ('a' -> 'b')
            char_p1 = chr(ord(char) + 1)
            first = self.binsearch(suffixes, offset, char, lo, hi)
            last = self.binsearch(suffixes, offset, char_p1, lo, hi)

            result += last - first
            lo, hi = first-1, last
        return result

if __name__ == '__main__':
    # f = open('string_similarity.in')
    f = sys.stdin
    T = int(f.readline())
    for i in xrange(T):
        s = f.readline()
        s = s.strip()
        solver = StringSimilarity(s)
        print solver.solve()