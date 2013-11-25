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

NO_BLOCK_UID = -1


class BruteForceStrategy(object):

    def get_next_states(self, state):
        """Given a game state, return all possible next states."""
        if state.phase == TurnPhase.DeclareAttackers:
            return self._get_next_states_when_attacking(state)
        elif state.phase == TurnPhase.DeclareBlockers:
            return self._get_next_states_when_blocking(state)

    def _get_next_states_when_attacking(self, state):
        # What creatures can attack?
        attacking_creature_uids = []
        for uid, creature in state.battleground.creatures_with_uids:
            if (creature.controlling_player == state.attacking_player and
                    not creature.tapped):
                attacking_creature_uids.append(uid)
        # Generate all possible attack assignments.
        subset_generator = get_all_subsets(attacking_creature_uids)
        for attacker_uids in subset_generator:
            next_state = copy.deepcopy(state)
            next_state.declare_attackers(attacker_uids)
            yield next_state

    def _get_next_states_when_blocking(self, state):
        # What creatures can block / what creatures are attacking?
        attacking_creature_uids = []
        blocking_creatures_uids = []
        for uid, creature in state.battleground.creatures_with_uids:
            if (creature.controlling_player == state.defending_player and
                    not creature.tapped):
                blocking_creatures_uids.append(uid)
            elif creature.attacking:
                attacking_creature_uids.append(uid)
        # Generate all possible blocking assignments, by adding a "0" uid
        # marking a fake attacker (representing a "no block").
        attacking_creature_uids.append(NO_BLOCK_UID)
        mappings_generator = \
            get_all_mappings(blocking_creatures_uids, attacking_creature_uids)
        for mapping in mappings_generator:
            # Remove NO_BLOCK_UID from mapping.
            for key in mapping.keys():
                if mapping[key] == NO_BLOCK_UID:
                    del mapping[key]
            next_state = copy.deepcopy(state)
            next_state.declare_blockers(mapping)
            yield next_state
