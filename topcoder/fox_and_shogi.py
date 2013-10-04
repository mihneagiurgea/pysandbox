class FoxAndShogi(object):

    def count(self, column):
        N = len(column)

        V = []
        pos = []
        for i in range(N):
            if column[i] != '.':
                V.append(column[i])
                pos.append(i)

        M = len(V)

        D = [[0] * N for _ in range(M+1)]
        if V[M-1] == 'D':
            for i in range(V[M-1], N):
                D[M-1][i] = 1
        else:
            for i in range(1, V[M-1]+1):
                D[M-1][i] = 1

        for i in range(M-2, -1, -1):
            for j in range(N, -1, -1):
                r = 0
                if V[i] == 'D':
                    if j < pos[i]:
                        r = D[i][j+1]
                    else:
                        r = sum(D[i+1][j+1:])
                else:
                    pass
                D[i][j] = r




    def differentOutcomes(self, board):
        pass