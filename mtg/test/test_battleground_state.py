import unittest

from battleground_state import BattlegroundState
from factories import BattlegroundStateFactory, CreatureStateFactory

class TestBattlegroundState(unittest.TestCase):

    SERIALIZATION_FIXTURES = (
        '2/3 (T), 4/6 vs 0/7',
        ' vs 0/7',
        ' vs '
    )

    def test_creature_accessor(self):
        """Test that the creatures can be accessed via their uid."""
        bg = BattlegroundStateFactory()
        h1 = bg.normalize()
        uid = bg.add_creature(CreatureStateFactory())

        bg[uid].tap()
        self.assertNotEqual(bg.normalize(), h1)

    def test_normalize(self):
        bg = BattlegroundState()
        h1 = bg.normalize()

        uid = bg.add_creature(CreatureStateFactory())
        h2 = bg.normalize()
        self.assertNotEqual(h1, h2)

        bg.remove_creature(uid)
        self.assertEqual(h1, bg.normalize())

    def test_equality_when_different_uids(self):
        """Test equality when creature uids differ."""
        bg1 = BattlegroundState()
        bg2 = BattlegroundState()

        uid1 = bg1.add_creature(CreatureStateFactory())
        bg1.remove_creature(uid1)

        creature_state = CreatureStateFactory()
        bg1.add_creature(creature_state)
        bg2.add_creature(creature_state)

        self.assertEqual(bg1, bg2)

    def test_equality_when_different_creature_order(self):
        """Test equality when creatures have been added in different orders."""
        bg1 = BattlegroundState()
        bg2 = BattlegroundState()

        creature_state1 = CreatureStateFactory()
        creature_state2 = CreatureStateFactory()

        bg1.add_creature(creature_state1)
        bg1.add_creature(creature_state2)

        bg2.add_creature(creature_state2)
        bg2.add_creature(creature_state1)

        self.assertEqual(bg1, bg2)

    def test_serialization(self):
        """Test repr and from_string methods together."""
        for s in self.SERIALIZATION_FIXTURES:
            self.assertEqual(repr(BattlegroundState.from_string(s)), s,
                             'Invalid deserialize & serialize transformation')
        for _ in range(10):
            state = BattlegroundStateFactory.build_with_creatures(9)
            s = repr(state)
            self.assertEqual(repr(BattlegroundState.from_string(s)), s,
                             'Invalid deserialize & serialize transformation')

    def test_get_creatures(self):
        bg = BattlegroundStateFactory.build_with_creatures(9)
        self.assertEqual(len(bg.creatures), 9)
        self.assertEqual(len(bg.get_creatures(0)) + len(bg.get_creatures(1)), 9)
