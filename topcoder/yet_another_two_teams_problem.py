class YetAnotherTwoTeamsProblem(object):

    def count(self, skill):
        """
        >>> obj = YetAnotherTwoTeamsProblem()
        >>> obj.count([5, 4, 7, 6])
        2
        >>> obj.count([1, 1, 1, 1, 1])
        10
        >>> obj.count([1, 2, 3, 5, 10])
        5
        >>> obj.count([1, 2, 3, 4, 10])
        0
        >>> obj.count([999, 999, 999, 1000, 1000, 1001, 999, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 999, 1000, 512, 511, 1001, 1001, 1001, 1001, 1001, 1000])
        17672631900
        >>> obj.count((56709, 32581, 23159, 40328, 14924, 22231, 14457, 53622, 14346, 55254, 58820, 57260, 14223, 12245, 28234, 56764, 32034, 34198, 54543, 27911, 37030, 33276, 48299, 54512, 53249, 8496, 23860, 35884, 33915, 599, 24252, 54549))
        47
        """
        S = sum(skill)
        half = (S + 1) / 2

        skill = list(skill)
        skill.sort(reverse=True)

        # D[i] = # of ways to form a team with skill-sum i
        D = [0 for _ in range(S+1)]
        for s in skill:
            for i in range(half-1, 0, -1):
                if D[i]:
                    D[i+s] += D[i]
            D[s] += 1

        result = 0
        for i in range(S+1):
            if 2 * i > S:
                result += D[i]
        return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()