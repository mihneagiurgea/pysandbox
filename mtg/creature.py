class Creature(object):
    """A stateless creature (i.e. a single Magic creature card or token).

    Attributes:
      * power
      * toughness
    """

    def __init__(self, power, toughness):
        if not (isinstance(power, int) and isinstance(toughness, int)):
            raise ValueError('Invalid power or toughness.')
        self.power = power
        self.toughness = toughness

    def normalize(self):
        """Normalizes this instance by converting it to a single integer."""
        return self.power << 5 | self.toughness

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.normalize() == other.normalize()
        return NotImplemented

    def __repr__(self):
        return '%d/%d' % (self.power, self.toughness)

    @classmethod
    def from_string(cls, string):
        p, t = string.strip().split('/')
        return Creature(int(p), int(t))

CreatureType = Creature