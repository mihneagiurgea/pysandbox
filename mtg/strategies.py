import copy

from turn_phase import TurnPhase


def get_all_subsets(S):
    """Given a set S, return all 2^||S|| subsets of S."""
    N = len(S)
    nr_subsets = 2 ** N
    for i in range(nr_subsets):
        subset = []
        for j in range(N):
            if i & (1 << j):
                subset.append(S[j])
        yield subset

def get_all_mappings(R, T):
    """Return all mappings f: R -> T such f is an arbitrary function
    (not necessary injective)."""
    N = len(R)
    M = len(T)
    nr_mappings = M ** N
    for i in range(nr_mappings):
        mapping = {}
        # Interpret i as a N-digit number in base M.
        for j in range(N):
            digit = i % M # between 0..M-1
            mapping[R[j]] = T[digit]
            i /= M
        yield mapping


class BruteForceStrategy(object):

    def get_next_states(self, state):
        """Given a game state, return all possible next states."""
        if state.phase == TurnPhase.DeclareAttackers:
            return self._get_next_states_when_attacking(state)

    def _get_next_states_when_attacking(self, state):
        subset_generator = get_all_subsets(state.attacking_player_creatures)
        for attackers in subset_generator:
            next_state = copy.deepcopy(state)
            next_state.declare_attackers(attackers)
            yield next_state

