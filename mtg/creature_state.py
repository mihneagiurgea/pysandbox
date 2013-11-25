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
        self.creature_type = creature_type
        self.controlling_player = controlling_player
        self.tapped = tapped
        self.attacking = attacking
        self.blocking = blocking

    def normalize(self):
        """Normalizes this instance by converting it to something hashable."""
        state = (int(self.blocking) << 3 | self.controlling_player << 2 |
                 int(self.tapped) << 1 | int(self.attacking))
        return (self.creature_type.normalize(), state)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.normalize() == other.normalize()
        return NotImplemented

    def __repr__(self):
        """Convert to a string, but ignores controlling_player information."""
        string = repr(self.creature_type)
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

    def __getattr__(self, name):
        """All CreatureType attributes should be accessible from a
        CreatureState instance."""
        return getattr(self.creature_type, name)

    def tap(self):
        self.tapped = True

    def untap(self):
        self.tapped = False

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
