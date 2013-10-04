class GUMIAndSongsDiv1(object):

    def maxSongs(self, duration, tone, T):
        """
        >>> obj = GUMIAndSongsDiv1()
        >>> obj.maxSongs((3, 5, 4, 11), (2, 1, 3, 1), 17)
        3
        >>> obj.maxSongs((100, 200, 300), (1, 2, 3), 99)
        0
        """
        N = len(duration)

        songs = [(duration[i], tone[i]) for i in range(N)]
        songs.sort(key=lambda s: s[1])

        # Use T+1 as +inf.
        inf = T+1

        D = [[inf] * (N+1) for _ in range(N+1)]

        max_songs = 0

        D[0][0] = 0
        D[0][1] = songs[0][0]

        for i in range(1, N):
            D[i][0] = 0
            for j in range(1, N+1):
                cost = inf
                for k in range(i):
                    cost_k = D[k][j-1]
                    if j > 1:
                        # Not the first song being played.
                        cost_k += songs[i][1] - songs[k][1]
                    cost = min(cost, cost_k)
                D[i][j] = cost + songs[i][0]
                if D[i][j] <= T:
                    max_songs = max(max_songs, j)

        return max_songs

import doctest
doctest.testmod()