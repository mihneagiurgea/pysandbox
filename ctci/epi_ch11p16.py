class ShiftingArray(object):

    def __init__(self, a):
        self.i = 0

    def head(self):
        return self.a[i]

    def advance(self):
        self.i += 1

def solve(a, b, c):
    sol = None
    arrays = [a, b, c]
    indexes = [0, 0, 0]
    while True:
        # Find minimum a[ai], b[bi], c[ci]
        current_elements = [arrays[i][indexes[i]] for i in range(3)]
        current_sol = max(current_elements) - min(current_elements)
        if sol is None or current_sol < sol:
            sol = current_sol

        min_index = 0
        for i in range(1, 3):
            if (indexes[i] < len(arrays[i]) and
                arrays[i][indexes[i]] < arrays[min_index][indexes[min_index]]):
                min_index = i
        indexes[min_index] += 1
        if indexes[min_index] == len(arrays[min_index]):
            break

    return sol

if __name__ == '__main__':
    A = [1, 102, 210, 304, 500]
    B = [10, 202, 304, 403, 510]
    C = [100, 205, 300, 400, 500]
    print solve(A, B, C)

