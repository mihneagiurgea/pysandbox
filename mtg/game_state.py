import copy
import re

from battleground_state import BattlegroundState
from combat_assignment import CombatAssignment
from creature import Creature
from turn_phase import TurnPhase


class GameState(object):
    """The game state, encoding players' lives and creatures.

    GameState is implemented as a mutable class - this means that it has
    methods that modify the given class, instead of returning an instance
    of a new class.

    Structure of a turn and how it relates to state:
    1) DeclareAttackersStep - during this step attackers are declared,
    one by one, via the .declare_attacker(uid) method. After this step
    the state of which creatures are attacking is kept in battleground, via
    CreatureState (an implied list).
    2) DeclareBlockersStep - during this step blockers declared (as blocking
    some attacking creature), via the .declare_blocker(uid) method. After this
    step the state of which creature blocks where, and which creature is
    not blocked is kept in battleground, via CreatureState => an implied mapping
        Map[ <attacking_creature> -> List[<blocking_creature>] ]
    3) CombatDamageStep - during this step the blockers must be ordered by
    the attacking player, via the .order_blockers() method. This will create
    an explicit mapping, which will represent the BlockingCreaturesOrder:
        Map[ <attacking_creature> -> List[<blocking_creature>] ].
    """

    def __init__(self):
        self.player_life = [20, 20]
        self.battleground = BattlegroundState()
        self.player_creatures = [ [], [] ]
        # This will point to a CombatAssignment object.
        self._combat_assignment = None
        self.active_player = 0
        self.phase = TurnPhase.DeclareAttackers

    def __repr__(self):
        """Converts to a string of the following form:
            <life0>/<life1> (<active_player>/<phase>): <battleground_state>

        E.g.:
            '20/18 (0/0): 2/3 (T), 4/6 vs 0/7'
            '20/-2 (0/2): vs 0/7'

        WARNING - this is not as strong as the .normalize() method.
        """
        if self.phase != TurnPhase.DeclareAttackers:
            raise NotImplementedError('Serialization is not implemented for this phase')

        return '%d/%d (%d/%d): %r' % (self.player_life[0], self.player_life[1],
                                      self.active_player, self.phase,
                                      self.battleground)

    _FROM_STRING_PATTERN = \
        '(?P<player0_life>.+)/(?P<player1_life>.+) ' \
        '\((?P<active_player>\d)/(?P<phase>\d)\): (?P<battleground>.*)'

    @classmethod
    def from_string(cls, string):
        match = re.match(cls._FROM_STRING_PATTERN, string)
        if not match:
            raise ValueError('Invalid string: %r' % string)
        params = match.groupdict()

        game_state = GameState()
        game_state.player_life[0] = int(params['player0_life'])
        game_state.player_life[1] = int(params['player1_life'])
        game_state.active_player = int(params['active_player'])
        game_state.phase = int(params['phase'])
        game_state.battleground = \
            BattlegroundState.from_string(params['battleground'])
        return game_state

    def add_creature(self, player, creature):
        """Add a creature under some player's control."""
        pass

    def remove_creature(self, player, creature):
        """Removes a creature from some player's control."""
        pass

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

    @property
    def all_creatures(self):
        return self.player_creatures[0] + self.player_creatures[1]

    def make_combat_assignment(self):
        return CombatAssignment(self)

    def untap(self):
        """Untap for active player."""
        for creature in self.player_creatures[self.active_player]:
            creature.untap()

    ### CombatPhase-related ###

    def _expect_step(self, expected_phase_or_step):
        if self.phase != expected_phase_or_step:
            raise ValueError('Invalid turn phase or step')
        # if not isinstance(combat_assignment, CombatAssignment):
        #     raise ValueError('Invalid combat_assignment argument')
        # if combat_assignment.game_state != self:
        #     raise ValueError('CombatAssignment argument should be associated '
        #                      ' with current game state')

    def declare_attackers(self, attacking_creature_uids):
        self._expect_step(TurnPhase.DeclareAttackers)
        if not self.is_valid_attack(attacking_creature_uids):
            raise ValueError('Invalid attack')

        if attacking_creature_uids:
            for uid in attacking_creature_uids:
                creature_state = self.battleground[uid]
                creature_state.attack()
                creature_state.tap()
            self.phase = TurnPhase.DeclareBlockers
        else:
            self.end_turn()

    def is_valid_attack(self, attacking_creature_uids):
        for uid in attacking_creature_uids:
            creature_state = self.battleground[uid]
            if creature_state.tapped:
                return False
            if creature_state.controlling_player != self.attacking_player:
                return False
        return True

    def declare_blockers(self, blocking_assignment):
        """
        Args:
            blocking_assignment: a map of <blocker_uid> -> <blocker_uid>
        """
        self._expect_step(TurnPhase.DeclareBlockers)
        if not self.is_valid_block(blocking_assignment):
            raise ValueError('Invalid blocking assignment')

        for blocker_uid, blocked_uid in blocking_assignment.items():
            blocker = self.battleground[blocker_uid]
            blocker.block(blocker_uid)

        self.phase = TurnPhase.CombatStep

    def is_valid_block(self, blocking_assignment):
        for blocker_uid, blocked_uid in blocking_assignment.items():
            blocker = self.battleground[blocker_uid]
            blocked = self.battleground[blocked_uid]
            # Tapped creatures cannot block.
            if blocker.tapped:
                return False
            # Only creatures controlled by defending player can block.
            if blocker.controlling_player != self.defending_player:
                return False
            # Can only block an attacking creature.
            if not blocked.attacking:
                return False
        return True

    def resolve_combat(self, combat_assignment):
        self._expect_step(TurnPhase.CombatStep)

        # TODO - check that combat_assignment is similar to the current one
        for attacker_uid, blocker_uids in combat_assignment.items():
            self._resolve_attacker(attacker_uid, blocker_uids)
        self.end_turn()

    def _resolve_attacker(self, attacker_uid, blocker_uids):
        if not blocker_uids:
            # Deal damage to defending player.
            self.player_life[self.defending_player] -= attacker_uid.power
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
        self.untap()
