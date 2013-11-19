import random

from creature import Creature
from game_state import GameState
from turn_phase import TurnPhase

def random_creature():
    # 0/0 up to 5/5
    return Creature(random.randint(0, 5),
                    random.randint(0, 5))

def random_game_state(nr_creatures=5, phase=TurnPhase.DeclareAttackers):
    if phase != TurnPhase.DeclareAttackers:
        raise NotImplementedError('Invalid phase')

    game_state = GameState()
    for i in range(nr_creatures):
        creature = random_creature()
        game_state.player_creatures[i%2].append(creature)

    return game_state


