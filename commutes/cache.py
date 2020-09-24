from typing import Any, NamedTuple

import os
import pickle
import time


class Cache(object):
    class TsValue(NamedTuple):
        ts: int
        value: Any

    def __init__(self, filename):
        self.filename = filename
        self.refresh()

    def refresh(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as file:
                self._state = pickle.load(file)
            print("Loaded state from %s: %d keys." % (self.filename, len(self._state)))
        else:
            self._state = {}
            print("File %s does not exist." % (self.filename,))

    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self._state, f)
        print("Saved state to %s: %d keys." % (self.filename, len(self._state)))

    def get(self, key, function):
        if key not in self._state:
            print("Cache miss for %s. Calling function..." % (key,))
            value = function(key)
            ts = int(time.time())
            self._state[key] = Cache.TsValue(ts, value)
            self.save()
        return self._state[key].value
