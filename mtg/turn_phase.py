class TurnPhase(object):

    ### Combat phase ###

    # The initial state, before attackers have been declared.
    DeclareAttackers = 0
    # Before blockers have been declared, but after attackers.
    DeclareBlockers = 1
    # CombatStep step, in which combat damage is dealt.
    CombatStep = 2

    # After the combat Phase, we'll skip directly to End of turn.
    EndOfTurn = 3