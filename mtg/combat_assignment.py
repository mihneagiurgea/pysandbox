from collections import defaultdict


class CombatAssignment(defaultdict):
    """Represents a complete combat assignment, including ordered blockers:
        Map[ <attacking_creature_uid> -> List[<blocking_creature_uids>] ]
    """

    def __init__(self, mapping=None):
        if mapping is None:
            mapping = {}
        super(CombatAssignment, self).__init__(list, mapping)

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
