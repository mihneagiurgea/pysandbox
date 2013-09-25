from collections import defaultdict
import threading


class Graph(object):

    def __init__(self):
        self._neighbours = defaultdict(set)
        self._visited = set()

    def add_arc(self, i, j):
        self._neighbours[i].add(j)

    def remove_arc(self, i, j):
        self._neighbours[i].remove(j)

    def path_exists(self, i, j):
        self._visited.clear()
        self._df(i)
        return j in self._visited

    def _df(self, node):
        self._visited.add(node)
        for i in self._neighbours[node]:
            if not self._visited[i]:
                self._df(i)


class LockState(object):

    def __init__(self):
        self._lock = threading.Lock()
        self.graph = Graph()

    def can_acquire(self, thread, lock):
        with self._lock:
            if self.graph.path_exists(lock, thread):
                return False
            return True

    def acquire(self, thread, lock):
        with self._lock:
            if not self.can_acquire(thread, lock):
                return False
            self.graph.add_arc(lock, thread)
            return True

    def release(self, thread, lock):
        with self._lock:
            self.graph.remove_arc(lock, thread)


class SmartLock(threading.Lock):

    lock_state = LockState()

    def acquire(self, blocking=True):
        if self.lock_state.acquire(threading.current_thread, self):
            return threading.Lock.acquire(self, blocking)
        else:
            return False

    def release(self):
        self.lock_state.release(threading.current_thread, self)
        return threading.Lock.release(self)


lock_state = LockState()
lock_state.acquire('thread1', 'lock1')
lock_state.acquire('thread2', 'lock2')
lock_state.acquire('thread2', 'lock1')



