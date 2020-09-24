import threading


class Node(object):

    def __init__(self, v, callback=None):
        self.v = v
        self.callback = callback
        self.children = {}  # name -> Node


class Tree(object):

    def __init__(self):
        self.tree = Node(None, None)
        self.root = self.tree  # "/"
        self._lock = threading.Lock()

    def _split_path(self, path):
        return path.split("/")[1:]

    def _find_node(self, path):
        node = self.root
        for token in self._split_path(path):
            if token not in node.children:
                return None
            node = node.children[token]
        return node

    def _trigger_calbacks(self, path):
        node = self.root
        # Note - this won't trigger callback for root.
        for token in self._split_path(path):
            node = node.children[token]
            if node.callback:
                node.callback("todo", node.v)

    def get(self, path):
        with self._lock:
            node = self._find_node(path)
            if node:
                return node.v

    def update(self, path, v):
        with self._lock:
            node = self._find_node(path)
            if node:
                node.v = v
            else:
                raise ValueError("No such path: {}".format(path))

            self._trigger_calbacks(path)

    def create(self, path, v):
        with self._lock:
            # "/a/b/c" -> ("/a/b", "c")
            parent_path, subpath = path.rsplit("/", 1)
            node = self._find_node(parent_path)
            if not node:
                raise ValueError("No such path: {}".format(parent_path))
            node.children[subpath] = Node(v=v)

            self._trigger_calbacks(path)

    def watch(self, path, callback):
        with self._lock:
            node = self._find_node(path)
            if not node:
                raise ValueError("No such path: {}".format(path))
            node.callback = callback


if __name__ == "__main__":
    t = Tree()
    print(t.get("/a/b/c"))
    t.create("/a", "1")
    t.create("/a/b", "2")
    t.create("/a/b/c", "3")
    print(t.get("/a/b/c"))
    t.update("/a/b/c", "4")
    print(t.get("/a/b/c"))

    def callback(path, v): return print("callback({}, {})".format(path, v))
    t.watch("/a/b", callback)

    t.update("/a/b/c", "5")
