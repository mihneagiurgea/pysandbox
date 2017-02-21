from collections import namedtuple

Rectangle = namedtuple("Rectangle", ["h", "l", "r"])
debug = False

def area(rect):
    return rect.h * (rect.r - rect.l + 1)

def maxarea(r1, r2):
    if debug: print "maxarea(%s, %s)" % (r1, r2)
    if area(r2) > area(r1):
        return r2
    else:
        return r1

class Solution(object):

    def largestRectangleArea(self, heights):
        """
        :type heights: List[int]
        :rtype: int
        """
        best = Rectangle(0, 0, 0)

        # Pad with 0s.
        heights.insert(0, 0)
        heights.append(0)
        idxs = []
        for idx, height in enumerate(heights):
            # Pop-right form idxs such that H[idxs[i]] >= height
            while idxs and heights[ idxs[-1] ] >= height:
                h = heights[idxs.pop()]
                if not idxs:
                    assert height == 0
                    left_idx = -1  # Irrelevant, since height = 0
                else:
                    left_idx = idxs[-1] + 1
                rect = Rectangle(h=h, l=left_idx, r=idx-1)
                best = maxarea(best, rect)
            idxs.append(idx)
            if debug: print "After %d: %s" % (height, idxs)
        return area(best)

print Solution().largestRectangleArea([2,1,5,6,0,2,3])




