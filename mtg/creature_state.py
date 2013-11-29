import re

from creature_type import CreatureType


class CreatureState(object):
    """Stateful representation of a creature, including all attributes.

    Each instance contains a reference to a CreatureType instance, to which
    it delegates unknown attributes (power, toughness, etc.).

    Attributes:
      * controller: int - which player controlls this
      * tapped: bool
      * attacking: bool
      * blocking: int - 0 if not blocking, otherwise = uid of blocked creature
      * ...and all CreatureType attributes...
    """

    def __init__(self, creature_type, controlling_player,
                 tapped=False, attacking=False, blocking=0):
        if not isinstance(creature_type, CreatureType):
            raise ValueError('Invalid creature_type argument: %r' %
                             creature_type)
        self._creature_type = creature_type
        self._state = self._pack(blocking, controlling_player,
                                  tapped, attacking)
        # self.controlling_player = controlling_player
        # self.tapped = tapped
        # self.attacking = attacking
        # self.blocking = blocking

    def copy(self):
        """Create a shallow of this object (no need to deepcopy the
        _creature_type reference)."""
        result = CreatureState(self._creature_type, self.controlling_player)
        result._state = self._state
        return result

    ATTACKING_MASK = 1
    TAPPED_MASK = 1 << 1
    CONTROLLING_PLAYER_MASK = 1 << 2
    BLOCKING_BIT_SHIFT = 3

    def _pack(self, blocking, controlling_player, tapped, attacking):
        return (blocking << 3 | controlling_player << 2 |
                tapped << 1 | attacking)

    @property
    def blocking(self):
        return self._state >> self.BLOCKING_BIT_SHIFT

    @blocking.setter
    def blocking(self, value):
        self._state = (value << self.BLOCKING_BIT_SHIFT) | (self._state & 7)

    @property
    def controlling_player(self):
        return 1 if self._state & self.CONTROLLING_PLAYER_MASK else 0

    @controlling_player.setter
    def controlling_player(self, value):
        if value:
            self._state |= self.CONTROLLING_PLAYER_MASK
        else:
            self._state &= ~self.CONTROLLING_PLAYER_MASK

    @property
    def tapped(self):
        return 1 if self._state & self.TAPPED_MASK else 0

    def tap(self):
        self._state |= self.TAPPED_MASK

    def untap(self):
        self._state &= ~self.TAPPED_MASK

    @property
    def attacking(self):
        return self._state & self.ATTACKING_MASK

    @attacking.setter
    def attacking(self, value):
        if value:
            self._state |= self.ATTACKING_MASK
        else:
            self._state &= ~self.ATTACKING_MASK

    def normalize(self):
        """Normalizes this instance by converting it to something hashable."""
        # state = (int(self.blocking) << 3 | self.controlling_player << 2 |
                 # int(self.tapped) << 1 | self.attacking)
        return (self._creature_type.normalize(), self._state)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.normalize() == other.normalize()
        return NotImplemented

    def __repr__(self):
        """Convert to a string, but ignores controlling_player information."""
        string = repr(self._creature_type)
        state = ''
        if self.tapped:
            state += 'T'
        if self.attacking:
            state += 'A'
        if self.blocking:
            state += 'B#%d' % self.blocking
        if state:
            string += ' (%s)' % state
        return string

    @classmethod
    def from_string(cls, string, controlling_player):
        if '(' in string:
            string, state_string = re.search('(.*) \((.*)\)', string).groups()
        else:
            state_string = ''
        creature_type = CreatureType.from_string(string)
        tapped = 'T' in state_string
        attacking = 'A' in state_string
        if 'B' in state_string:
            blocking = int(re.search('B#(\d+)', state_string).group(1))
        else:
            blocking = 0

        return CreatureState(creature_type, controlling_player,
            tapped=tapped, attacking=attacking, blocking=blocking)

    # CreatureType attributes
    # Explicitly defining them is a lot faster than using __getattr__
    @property
    def power(self):
        return self._creature_type.power

    @property
    def toughness(self):
        return self._creature_type.toughness

    # def tap(self):
    #     self.tapped = True

    # def untap(self):
    #     self.tapped = False

    def attack(self):
        if self.tapped:
            raise ValueError('Tapped creatures cannot attack')
        self.attacking = True

    def block(self, uid):
        if self.tapped:
            raise ValueError('Tapped creatures cannot block')
        if not (isinstance(uid, int) and uid > 0):
            raise ValueError('Invalid uid argument: %r' % uid)
        self.blocking = uid

    def remove_from_combat(self):
        self.attacking = False
        self.blocking = 0
