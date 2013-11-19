import copy
import re

from combat_assignment import CombatAssignment
from creature import Creature
from turn_phase import TurnPhase


class GameState(object):
    """The game state, encoding players' lives and creatures.

    GameState is implemented as a mutable class - this means that it has
    methods that modify the given class, instead of returning an instance
    of a new class.

    Attributes and their meaning:
      * phase - roughly encodes the current game phase for the current turn:
        0 - beginning of turn
        1 - attackers have been declared (at least 1)
        2 - blockers have been declared
    """

    def __init__(self):
        self.player_life = [20, 20]
        self.player_creatures = [ [], [] ]
        # This will point to a CombatAssignment object.
        self._combat_assignment = None
        self.active_player = 0
        self.phase = TurnPhase.DeclareAttackers
        # This is strictly informative.
        self.current_turn_number = 1

    FROM_STRING_PATTERN = \
        '(?P<player0_life>.+)/(?P<player1_life>.+) ' \
        '\((?P<active_player>\d)/(?P<phase>\d)\): ' \
        '(?P<player0_creatures>.*)vs(?P<player1_creatures>.*)'
    _CREATURE_SEPARATOR = ', '

    @classmethod
    def from_string(cls, string):
        match = re.match(cls.FROM_STRING_PATTERN, string)
        if not match:
            raise ValueError('Invalid string: %r' % string)
        state = match.groupdict()
        game_state = GameState()
        game_state.player_life[0] = int(state['player0_life'])
        game_state.player_life[1] = int(state['player1_life'])
        game_state.active_player = int(state['active_player'])
        game_state.phase = int(state['phase'])
        for player in (0, 1):
            string = state['player%d_creatures' % player].strip()
            if not string:
                continue
            for creature_string in string.split(cls._CREATURE_SEPARATOR):
                creature = Creature.from_string(creature_string)
                game_state.player_creatures[player].append(creature)
        return game_state

    def __repr__(self):
        """

        Life1/Life2 (active_player/phase) <player_creatures[0]> vs <player_creatures[1]>

        E.g.:
            20/18 (0/0): 2/3 (T), 4/6 vs 0/7
            20/-2 (0/2): vs 0/7
        """
        if self.phase != TurnPhase.DeclareAttackers:
            raise NotImplementedError('Serialization is not implemented for this phase')
        player0_creatures = self._CREATURE_SEPARATOR.join(map(repr, self.player_creatures[0]))
        player1_creatures = self._CREATURE_SEPARATOR.join(map(repr, self.player_creatures[1]))
        return '%d/%d (%d/%d): %s vs %s' % \
            (self.player_life[0], self.player_life[1], self.active_player,
             self.phase, player0_creatures, player1_creatures)

    @property
    def attacking_player(self):
        return self.active_player

    @property
    def defending_player(self):
        return 1 - self.active_player

    @property
    def attacking_player_creatures(self):
        return self.player_creatures[self.attacking_player]

    @property
    def defending_player_creatures(self):
        return self.player_creatures[self.defending_player]

    def _expect_step(self, expected_phase_or_step, combat_assignment):
        if self.phase != expected_phase_or_step:
            raise ValueError('Invalid turn phase or step')
        if not isinstance(combat_assignment, CombatAssignment):
            raise ValueError('Invalid combat_assignment argument')
        if combat_assignment.game_state != self:
            raise ValueError('CombatAssignment argument should be associated '
                             ' with current game state')

    def make_combat_assignment(self):
        return CombatAssignment(self)

    def untap(self):
        """Untap for active player."""
        for creature in self.player_creatures[self.active_player]:
            creature.untap()

    def declare_attackers(self, combat_assignment):
        self._expect_step(TurnPhase.DeclareAttackers, combat_assignment)

        if combat_assignment.attacking_creatures:
            self.phase = TurnPhase.DeclareBlockers
            for creature in combat_assignment.attacking_creatures:
                creature.tap()
            # Is this really needed?
            self._combat_assignment = copy.deepcopy(combat_assignment)

        else:
            self.end_turn()

    def declare_blockers(self, combat_assignment):
        self._expect_step(TurnPhase.DeclareBlockers, combat_assignment)

        self.phase = TurnPhase.CombatStep
        # Is this really needed?
        self._combat_assignment = copy.deepcopy(combat_assignment)

    def resolve_combat(self, combat_assignment):
        self._expect_step(TurnPhase.CombatStep, combat_assignment)

        for attacking_creature, blockers in combat_assignment.assignment.items():
            self._resolve_attacker(attacking_creature, blockers)
        self.end_turn()

    def _resolve_attacker(self, attacking_creature, blockers):
        if not blockers:
            # Deal damage to defending player.
            self.player_life[self.defending_player] -= attacking_creature.power
            return

        attacker_damage = attacking_creature.power
        for blocker in blockers:
            if attacker_damage >= blocker.toughness:
                attacker_damage -= blocker.toughness
                # Blocker has died, remove it from current state.
                self.player_creatures[self.defending_player].remove(blocker)
            else:
                break
        blockers_damage = sum(blocker.power for blocker in blockers)
        if blockers_damage >= attacking_creature.toughness:
            self.player_creatures[self.active_player].remove(attacking_creature)

    def end_turn(self):
        """End the current turn, and pass turn to the other player."""
        self.active_player = 1 - self.active_player
        self._combat_assignment = None
        self.phase = TurnPhase.DeclareAttackers
        self.current_turn_number += 1
        self.untap()
