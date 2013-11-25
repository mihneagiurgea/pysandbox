import re

from combat_assignment import CombatAssignment
from creature_state import CreatureState


class BattlegroundState(object):
    """Stateful representation of all creatures currently on the battleground.

    When a new creature enters the battleground, it is assigned a unique id,
    which will never change (even if the creature changes its controller).
    Attributes:
      *
      * maintains information related to all creatures currently on the battleground
      * this class knows about creature uids
      * uids should not change while modifying the state

    """

    def __init__(self):
        self._uid_to_creature_state = {}
        self._next_uid = 1

    def normalize(self):
        """Normalize this instance by converting it to something hashable."""
        tuples = []
        for creature_state in self._uid_to_creature_state.values():
            # Normalize each creature state.
            tuples.append(creature_state.normalize())
        # Sort tuples to eliminate the order of the creatures as a
        # differentiating factor between battleground states.
        tuples.sort()
        return tuple(tuples)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.normalize() == other.normalize()
        return NotImplemented

    _FROM_STRING_PATTERN = '(?P<player0_creatures>.*)vs(?P<player1_creatures>.*)'
    _CREATURE_SEPARATOR = ', '

    def __repr__(self):
        """Converts to a string: <player0_creatures> vs <player1_creatures>.

        E.g.:
            '2/3 (T), 4/6 vs 0/7'
            ' vs 0/7'

        WARNING - this is not as strong as the .normalize() method.
        """
        creatures = ([], [])
        for creature_state in self._uid_to_creature_state.values():
            s = repr(creature_state)
            creatures[creature_state.controlling_player].append(s)
        player0 = self._CREATURE_SEPARATOR.join(creatures[0])
        player1 = self._CREATURE_SEPARATOR.join(creatures[1])
        return '%s vs %s' % (player0, player1)

    @classmethod
    def from_string(cls, string):
        match = re.match(cls._FROM_STRING_PATTERN, string)
        if not match:
            raise ValueError('Invalid string: %r' % string)
        params = match.groupdict()

        battleground_state = BattlegroundState()
        for player in (0, 1):
            string = params['player%d_creatures' % player].strip()
            if not string:
                continue
            for creature_string in string.split(cls._CREATURE_SEPARATOR):
                creature_state = CreatureState.from_string(creature_string,
                                                           player)
                battleground_state.add_creature(creature_state)
        return battleground_state

    def __getitem__(self, uid):
        """Returns the CreatureState instance associated to the given uid."""
        return self._uid_to_creature_state[uid]

    @property
    def creatures(self):
        return self._uid_to_creature_state.values()

    @property
    def creatures_with_uids(self):
        return self._uid_to_creature_state.items()

    def get_creatures(self, controlling_player):
        result = []
        for creature in self.creatures:
            if creature.controlling_player == controlling_player:
                result.append(creature)
        return result

    def add_creature(self, creature_state):
        if not isinstance(creature_state, CreatureState):
            raise ValueError('Invalid type: %r' % creature_state)

        self._uid_to_creature_state[self._next_uid] = creature_state
        self._next_uid += 1

        return self._next_uid - 1

    def remove_creature(self, uid):
        del self._uid_to_creature_state[uid]

    # Do we still need this?
    def get_combat_assignment(self):
        """Returns the current combat assignment (how blockers are ordered).

        Returns:
            A dict { <attacker_uid> -> List[<blocker_uids>] }
        """
        combat_assignment = CombatAssignment()
        for uid, state in self._uid_to_creature_state.items():
            if state.attacking:
                # Touch uid to create an empty list.
                combat_assignment[uid]
            elif state.blocking:
                combat_assignment[state.blocking].append(uid)
        return combat_assignment
