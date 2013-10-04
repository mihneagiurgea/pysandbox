class LittleElephantAndBalls(object):

    def getNumber(self, S):
        result = 0
        count = { }
        for s in S:
            result += count.values()
            if s not in count:
                count[s] = 1
            else:
                count[s] = 2
        return result
