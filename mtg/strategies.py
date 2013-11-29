from combat_assignment import CombatAssignment
import combinatorics
from turn_phase import TurnPhase

NO_BLOCK_UID = -1


class BruteForceStrategy(object):

    def get_next_states(self, state):
        """Given a game state, return all possible next states."""
        if state.phase == TurnPhase.DeclareAttackers:
            return self._get_next_states_when_attacking(state)
        elif state.phase == TurnPhase.DeclareBlockers:
            return self._get_next_states_when_blocking(state)
        else:
            return self._get_next_states_when_ordering_blockers(state)

    def _get_next_states_when_attacking(self, state):
        # What creatures can attack?
        attacking_creature_uids = []
        for uid, creature in state.battleground.creatures_with_uids:
            if (creature.controlling_player == state.attacking_player and
                    not creature.tapped):
                attacking_creature_uids.append(uid)
        # Generate all possible attack assignments.
        subset_generator = \
            combinatorics.get_all_subsets(attacking_creature_uids)
        for attacker_uids in subset_generator:
            next_state = state.copy()
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
            combinatorics.get_all_mappings(blocking_creatures_uids,
                                           attacking_creature_uids)
        for mapping in mappings_generator:
            # Remove NO_BLOCK_UID from mapping.
            for key in mapping.keys():
                if mapping[key] == NO_BLOCK_UID:
                    del mapping[key]
            next_state = state.copy()
            next_state.declare_blockers(mapping)
            yield next_state

    def _get_next_states_when_ordering_blockers(self, state):
        unordered_combat_assignment = state.battleground.get_combat_assignment()
        mappings_generator = \
            combinatorics.get_all_shuffled_mappings(unordered_combat_assignment)
        for mapping in mappings_generator:
            combat_assignment = CombatAssignment(mapping)
            next_state = state.copy()
            next_state.resolve_combat(combat_assignment)
            yield next_state
