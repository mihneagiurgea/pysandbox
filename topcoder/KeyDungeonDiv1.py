from collections import namedtuple, defaultdict

State = namedtuple('State', ['r', 'g', 'w'])

class KeyDungeonDiv1(object):

    def canOpen(self, state, i):
        r = max(0, self.doorR[i] - state.r)
        g = max(0, self.doorG[i] - state.g)
        return state.w >= r + g

    def open(self, state, i):
        r = max(0, self.doorR[i] - state.r)
        g = max(0, self.doorG[i] - state.g)
        if state.w < r + g:
            # Cannot open this room.
            return None
        return State(r=max(0, state.r - self.doorR[i]) + self.roomR[i],
                     g=max(0, state.g - self.doorG[i]) + self.roomG[i],
                     w=state.w - r - g + self.roomW[i])

    def minimizeStates(self, states):
        w_to_states = defaultdict(list)
        for state in states:
            w_to_states[state.w].append(state)

        result = []
        for w in w_to_states:
            sub_states = w_to_states[w]
            sub_states.sort()
            prev = State(-1, -1, -1)
            for state in sub_states:
                if not (state.g >= prev.g):
                    result.append(prev)
                prev = state
            result.append(prev)
        return set(result)

    def maxKeys(self, doorR, doorG, roomR, roomG, roomW, keys):
        """
        >>> obj = KeyDungeonDiv1()
        >>> obj.maxKeys((1, 2, 3), (0, 4, 9), (0, 0, 10), (0, 8, 9), (1, 0, 8), (3, 1, 2))
        8
        >>> obj.maxKeys((1, 1, 1, 2), (0, 2, 3, 1), (2, 1, 0, 4), (1, 3, 3, 1), (1, 0, 2, 1), (0, 4, 0))
        4
        >>> obj.maxKeys((2, 0, 4), (3, 0, 4), (0, 0, 9), (0, 0, 9), (8, 5, 9), (0, 0, 0))
        27
        """
        self.doorR = doorR
        self.doorG = doorG
        self.roomR = roomR
        self.roomG = roomG
        self.roomW = roomW

        initial_state = State(*keys)
        states = set([initial_state])

        N = len(doorR)
        for i in range(N):
            new_states = set()
            for state in states:
                next_state = self.open(state, i)
                if next_state is not None:
                    new_states.add(next_state)

            states.update(new_states)

            # Minimize states.
            states = self.minimizeStates(states)

        max_keys = -1
        for state in states:
            max_keys = max(max_keys, state.r + state.g + state.w)
        return max_keys

import doctest
doctest.testmod()