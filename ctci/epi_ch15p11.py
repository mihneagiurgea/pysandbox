import threading

def f(x):
    return x / 2 if x % 2 == 0 else 3 * x + 1

class SyncedCache(object):

    def __init__(self):
        self._cache = {}
        self.lock = threading.Lock()

    def set(self, key, value):
        with self.lock:
            self._cache[key] = value

    def get(self, key, default=None):
        return self._cache.get(key, default)


class Worker(threading.Thread):

    def __init__(self, cache, queue):
        self.cache = cache
        self.queue = queue

    def run(self):
        for item in self.queue:
            lower, upper = item
            for n in range(lower, upper):
                self.solve(n)

    def solve(self, n):
        r = self.cache.get(n)
        if r is None:
            r = self.solve(f(n))
            self.cache.set(n, r)
        return r
