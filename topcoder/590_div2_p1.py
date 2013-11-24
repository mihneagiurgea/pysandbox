DX = [-1, -1, 0, 1, 1, 1, 0, -1]
DY = [0, 1, 1, 1, 0, -1, -1, -1]

class FoxAndGomoku(object):

    def win(self, board):
        if self.exists(board):
            return "found"
        else:
            return "not found"

    def exists(self, board):
        N = len(board)
        M = len(board[0])
        for i in range(N):
            for j in range(M):
                if board[i][j] != 'o':
                    continue

                for d in range(8):
                    cnt = 0
                    for l in range(1, 5):
                        x = i + DX[d] * l
                        y = j + DY[d] * l
                        if 0 <= x and x < N and 0 <= y and y < M and \
                            board[x][y] == 'o':
                            cnt += 1
                        else:
                            break
                    if cnt == 4:
                        return True
        return False


board = [
    "oooo.",
    ".oooo",
    "oooo.",
    ".oooo",
    "....."
]
obj = FoxAndGomoku()
print obj.win(board)