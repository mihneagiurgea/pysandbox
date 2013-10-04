class TheTree(object):

    def maximumDiameter(self, cnt):
        """

        >>> obj = TheTree()
        >>> obj.maximumDiameter((3, ))
        2
        >>> obj.maximumDiameter((2, 2))
        4
        >>> obj.maximumDiameter((4, 1, 2, 4))
        5
        >>> obj.maximumDiameter((4, 2, 1, 3, 2, 5, 7, 2, 4, 5, 2, 3, 1, 13, 6))
        21
        """
        D = len(cnt)
        result = D
        next_stop = D
        for i in range(len(cnt)-1, -1, -1):
            if cnt[i] == 1:
                next_stop = i
            else:
                diam = next_stop - i + D - i
                result = max(result, diam)
        return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()