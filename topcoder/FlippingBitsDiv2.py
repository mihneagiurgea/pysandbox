class FlippingBitsDiv2(object):

    def dp(self, S, M):
        # D[i][b] = min number of moves to convert first i * M bits from S
        # into all bits equal to b.
        D = [[0, 0] for _ in range(len(S) / M + 1)]
        for i in range(1, len(S) / M + 1):
            ones = S[(i-1) * M:i*M].count('1')
            for b in (0, 1):
                # Flip individual bits.
                to_flip = ones if b == 0 else M - ones
                res = D[i-1][b] + to_flip
                res = min(res, D[i-1][1-b] + (M - to_flip) + 1)
                D[i][b] = res
        return [row[1] for row in D]

    def getmin(self, S, M):
        """
        >>> obj = FlippingBitsDiv2()
        >>> obj.getmin(("00111000", ), 1)
        2
        >>> obj.getmin(("00111000", ), 2)
        3
        >>> obj.getmin(("111111", ), 3)
        0
        """
        S = ''.join(S)

        D = self.dp(S, M)
        E = self.dp(S[::-1], M)
        E = E[::-1]

        result = len(S)
        K = len(S) / M
        for i in range(K + 1):
            result = min(result, D[i] + E[i])
        return result




import doctest
doctest.testmod()