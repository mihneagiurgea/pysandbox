from collections import defaultdict


class CombatAssignment(defaultdict):
    """Represents a complete combat assignment, including ordered blockers:
        Map[ <attacking_creature_uid> -> tuple[ <blocking_creature_uids> ] ]

    E.g.:
    {
        # Blocked by a single creature
        1: (4, ),
        # Blocked by multiple creatures (in this order)
        2: (5, 6),
        # Unblocked
        3: ()
    }
    """

    def __init__(self, mapping=None):
        if mapping is None:
            mapping = {}
        # Convert lists to tuples.
        for key in mapping.keys():
            if isinstance(mapping[key], list):
                mapping[key] = tuple(mapping[key])
        super(CombatAssignment, self).__init__(tuple, mapping)

    def is_reorder_of(self, other):
        """Returns True if self can be obtained from other by reordering
        blockers, False otherwise.
        """
        if not isinstance(other, CombatAssignment):
            raise ValueError('Invalid other argument: %r' % other)
        if len(self) != len(other):
            return False
        for key in self:
            if key not in other:
                return False
            if sorted(self[key]) != sorted(other[key]):
                return False
        return True
