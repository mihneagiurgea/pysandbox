from collections import deque

DX = [-1, 0, 1, 0]
DY = [0, 1, 0, -1]

class FoxAndGo(object):

    def lee(self, board, visited, x, y):
        N = len(board)

        q = deque()
        q.append((x, y))
        visited.add((x, y))

        count = 0
        safe = False
        while q:
            x, y = q.popleft()
            count += 1

            for d in range(4):
                nx = x + DX[d]
                ny = y + DY[d]
                if 0 <= nx and nx < N and 0 <= ny and ny < N:
                    if board[nx][ny] == '.':
                        safe = True
                    elif board[nx][ny] == 'o' and (nx, ny) not in visited:
                        q.append((nx, ny))
                        visited.add((nx, ny))

        return 0 if safe else count

    def get_killed(self, board):
        N = len(board)

        killed = 0
        visited = set()
        for i in range(N):
            for j in range(N):
                if board[i][j] == 'o' and (i, j) not in visited:
                    killed += self.lee(board, visited, i, j)
        return killed

    def maxKill(self, board):
        copy = []
        for row in board:
            copy.append(list(row))
        board = copy

        N = len(board)
        best = 0
        for i in range(N):
            for j in range(N):
                if board[i][j] == '.':
                    board[i][j] = 'x'
                    kill = self.get_killed(board)
                    board[i][j] = '.'

                    best = max(best, kill)
        return best