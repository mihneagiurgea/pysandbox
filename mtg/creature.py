class Creature(object):

    def __init__(self, power, toughness, tapped=False):
        if not (isinstance(power, int) and isinstance(toughness, int)):
            raise ValueError('Invalid power or toughness.')
        self.power = power
        self.toughness = toughness
        self.tapped = tapped

    def tap(self):
        self.tapped = True

    def untap(self):
        self.tapped = False

    @classmethod
    def from_string(cls, string):
        tapped = False
        if 'T' in string:
            tapped = True
            string = string.split(' ')[0]
        p, t = map(int, string.strip().split('/'))
        return Creature(p, t, tapped=tapped)

    def __repr__(self):
        s = '%d/%d' % (self.power, self.toughness)
        if self.tapped:
            s = '%s (T)' % s
        return s

