def solve(A):
    A.insert(0, 0)

    # Compute prefix sums of A.
    prefix_sum = []
    curr_prefix = 0
    for a in A:
        curr_prefix += a
        prefix_sum.append(curr_prefix)

    # D[i] = max fill volume for A[0]...A[i].
    D = [0] * len(A)
    # Holds peaks in a stack, in decreasing order.
    peaks = []
    for i, a in enumerate(A):
        j = i - 1
        while peaks and A[peaks[-1]] < a:
            j = peaks.pop()
        if peaks:
            j = peaks[-1]
        peaks.append(i)

        fill = (i - j - 1) * min(A[i], A[j]) - (prefix_sum[i-1] - prefix_sum[j])
        D[i] = fill + D[j]
    print ['%2d' % x for x in A]
    print ['%2d' % x for x in D]
    return D[-1]

def main():
    A = [0,1,0,2,1,0,1,3,2,1,2,1]
    A = [10, 0, 0, 0, 7, 4, 0, 1, 0, 1, 6, 0, 1, 2]
    print solve(A)

if __name__ == '__main__':
    main()