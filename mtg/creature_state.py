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

    def __init__(self, creature_type, controlling_player, tapped=False):
        if not isinstance(creature_type, CreatureType):
            raise ValueError('Invalid creature_type argument: %r' %
                             creature_type)
        self.creature_type = creature_type
        self.controlling_player = controlling_player
        self.tapped = tapped
        self.attacking = False
        self.blocking = 0

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
        if self.tapped:
            string += ' (T)'
        return string

    @classmethod
    def from_string(cls, string, controlling_player):
        tapped = 'T' in string
        if tapped:
            string = string[:-4]
        creature_type = CreatureType.from_string(string)
        return CreatureState(creature_type, controlling_player, tapped=tapped)

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
