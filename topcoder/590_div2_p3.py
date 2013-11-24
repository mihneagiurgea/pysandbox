class FoxAndShogi(object):

    MODULO = 1000000007

    def countOutcomes(self, row):
        """
        >>> obj = FoxAndShogi()
        >>> obj.countOutcomes('LR')
        1
        >>> obj.countOutcomes('R.L.')
        3
        >>> obj.countOutcomes('R..L')
        6
        """
        N = len(row)
        M = N - row.count('.')
        if M == 0:
            return 1

        pos = []
        piece = []
        for i in range(N-1, -1, -1):
            if row[i] != '.':
                piece.append(row[i])
                pos.append(i)

        prev = None

        for i in range(M):
            lower = 0
            upper = N-1
            if piece[i] == 'R':
                lower = pos[i]
            else:
                upper = pos[i]
            curr = [0] * N
            for j in range(lower, upper+1):
                # Init.
                if i == 0:
                    curr[j] = 1
                else:
                    for l in range(j+1, N):
                        curr[j] += prev[l]
                    curr[j] %= self.MODULO

            prev = curr
        return sum(prev) % self.MODULO

    def differentOutcomes(self, board):
        result = 1
        N = len(board)
        for i in range(N):
            column = [board[j][i] for j in range(N)]
            column = ''.join(column)
            column = column.replace('D', 'R').replace('U', 'L')
            x = self.countOutcomes(column)
            result = (result * x) % self.MODULO
        return result


import doctest
doctest.testmod()