class CombatAssignment(object):
    """

    def __init__(self, game_state):
        self.game_state = game_state
        # Map[AttackingCreature -> List[BlockingCreature]]
        self.assignment = {}

    @property
    def attacking_creatures(self):
        return self.assignment.keys()

    def declare_attacker(self, creature):
        # Is this a valid attack?
        if creature.tapped:
            raise ValueError('Tapped creatures cannot attack.')
        if creature not in self.game_state.attacking_player_creatures:
            raise ValueError('Invalid attacker: %r' % creature)
        self.assignment[creature] = []

    def declare_blocker(self, creature, attacking_creature):
        # Is this a valid block?
        if creature.tapped:
            raise ValueError('Tapped creatures cannot attack.')
        if creature not in self.game_state.defending_player_creatures:
            raise ValueError('Invalid blocker: %r' % creature)
        if attacking_creature not in self.assignment:
            raise ValueError('Invalid attacking creature: %r' %
                             attacking_creature)
        self.assignment[attacking_creature].append(creature)

    def order_blockers(self, attacking_creature, blocking_creatures):
        # Is this a valid ordering of blockers?
        if attacking_creature not in self.assignment:
            raise ValueError('Invalid attacking creature: %r' %
                             attacking_creature)
        if set(blocking_creatures) != set(self.assignment[attacking_creature]):
            raise ValueError('Invalid reordering of blockers: %r' %
                             blocking_creatures)
        self.assignment[attacking_creature] = blocking_creatures
    """
    pass
