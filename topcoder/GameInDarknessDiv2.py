DX = (0, 1, 0, -1)
DY = (-1, 0, +1, 0)

DIR = {
    'U': 3,
    'R': 2,
    'D': 1,
    'L': 0
}

def move(p, d):
    return (p[0] + DX[d], p[1] + DY[d])

class GameInDarknessDiv2(object):

    def isEmpty(self, p):
        return 0 <= p[0] < self.N and 0 <= p[1] < self.M and \
               self.field[p[0]][p[1]] != '#'

    def f(self, bob, k):
        if k >= len(self.alice_at):
            # Alice gives up.
            return True

        alice_at = self.alice_at[k]
        if bob == alice_at:
            # Alice just won.
            return False

        # Try to move, Bob!
        for d in range(4):
            next_bob = move(bob, d)
            if self.isEmpty(next_bob) and next_bob != alice_at and self.canBobWin(next_bob, k+1):
                return True
        return False

    def canBobWin(self, bob, k):
        cache_key = (bob, k)
        if cache_key not in self._cache:
            # Compute result of this function call.
            self._cache[cache_key] = self.f(bob, k)
            # print 'f(%r, %d) = %r' % (bob, k, self._cache[cache_key])
        return self._cache[cache_key]

    def check(self, field, moves):
        self.field = field
        moves = ''.join(moves)

        alice_start = None
        bob_start = None
        self.N = len(field)
        self.M = len(field[0])
        for i in range(self.N):
            for j in range(self.M):
                if field[i][j] == 'A':
                    alice_start = (i, j)
                elif field[i][j] == 'B':
                    bob_start = (i, j)

        p = alice_start
        self.alice_at = [p]
        for m in moves:
            p = move(p, DIR[m])
            self.alice_at.append(p)

        self._cache = {}
        can_bob_win = self.canBobWin(bob_start, 1)
        return "Bob wins" if can_bob_win else "Alice wins"

if __name__ == '__main__':
    # {{"A.B..", "##.##", "##.##"}, {"RRDUR"}}
    field = (
        "A.B..",
        "##.##",
        "##.##"
    )
    moves = ("RRDUR", )
    obj = GameInDarknessDiv2()
    print obj.check(field, moves)