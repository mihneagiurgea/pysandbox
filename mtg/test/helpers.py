import random

from creature import Creature
from creature_state import CreatureState
from battleground_state import BattlegroundState
from game_state import GameState
from turn_phase import TurnPhase

def random_creature(power=None, toughness=None):
    # 0/0 up to 5/5
    if power is None:
        power = random.randint(0, 5)
    if toughness is None:
        toughness = random.randint(0, 5)
    return Creature(power, toughness)

def random_creature_state(controlling_player=None):
    if controlling_player is None:
        controlling_player = random.randint(0, 1)
    return CreatureState(controlling_player, bool(random.randint(0, 1)))

def random_battleground_state(nr_creatures=9):
    state = BattlegroundState()
    for i in range(nr_creatures):
        state.add_creature(random_creature(), random_creature_state())
    return state

def random_game_state(nr_creatures=9, phase=TurnPhase.DeclareAttackers):
    if phase != TurnPhase.DeclareAttackers:
        raise NotImplementedError('Invalid phase')

    game_state = GameState()
    game_state.player_life = [random.randint(-6, 20), random.randint(-6, 20)]
    game_state.battleground = random_battleground_state(nr_creatures)
    return game_state
