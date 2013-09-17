class LRUCache(object):

    def __init__(self, size=100):
        self.size = size
        self._store = {}
        # Hold a doubly linked list of keys, sorted in order of least-recently
        # used.
        self._next = {}
        self._prev = {}
        # First and last keys from the doubly linked list.
        self._first = None
        self._last = None

    def __len__(self):
        return len(self._store)

    def _refresh(self, key):
        """Marks this key as "just used", by moving it in the top of the
        least-recently used linked list.
        """
        # If this key is already the last one, don't do anything.
        if self._last == key:
            return
        # Is the linked list empty?
        if self._last is None:
            self._first = key
        else:
            # Is the key anywhere in the list? If so, remove it from the list,
            # then add it at the end.
            if key in self._next:
                if self._prev[key]:
                    self._next[self._prev[key]] = self._next[key]
                if self._next[key]:
                    self._prev[self._next[key]] = self._prev[key]
            # Add key at the end of the list.
            self._next[self._last] = key
            # Do we need to update the `first` pointer?
            if self._first == key:
                self._first = self._next[self._first]
        # Make key the last key in the list.
        self._prev[key] = self._last
        self._next[key] = None
        self._last = key

    def _evict(self):
        """Evicts the least-recently used key."""
        if self._first is None:
            raise IndexError('evict from empty list')
        next_key = self._next[self._first]
        if next_key:
            self._prev[next_key] = None
        else:
            # Just evicted the last key - cache is now empty.
            self._last = None
        del self._store[self._first]
        del self._next[self._first]
        del self._prev[self._first]
        self._first = next_key

    def bound(self, size):
        self.size = size
        while len(self) > self.size:
            self._evict()

    def set(self, key, value):
        self._store[key] = value
        self._refresh(key)
        if len(self) > self.size:
            self._evict()

    def get(self, key, default=None):
        if key not in self._store:
            return default
        self._refresh(key)
        return self._store[key]

    def peek(self, key, default=None):
        return self._store.get(key, default)

    def dump(self):
        return self._store.items()


def solve(f):
    N = int(f.readline())
    cache = LRUCache()
    while N:
        N -= 1
        strarr = f.readline().split()
        if strarr[0] == 'BOUND':
            cache.bound(int(strarr[1]))
        elif strarr[0] == 'SET':
            cache.set(strarr[1], strarr[2])
        elif strarr[0] == 'GET':
            print cache.get(strarr[1], 'NULL')
        elif strarr[0] == 'PEEK':
            print cache.peek(strarr[1], 'NULL')
        else:
            items = cache.dump()
            items.sort()
            for item in items:
                print '%s %s' % item


if __name__ == '__main__':
    import sys
    f = sys.stdin
    f = open('lru_cache.in', 'r')
    solve(f)
