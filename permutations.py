def apply_perm(A, P):
    """
    >>> A = ['a', 'b', 'c', 'd', 'e']
    >>> apply_perm(A, [3, 1, 2, 5, 4])
    >>> A
    ['b', 'c', 'a', 'e', 'd']
    >>> apply_perm(A, [2, 3, 1, 5, 4])
    >>> A
    ['a', 'b', 'c', 'd', 'e']
    >>> A = ['a', 'b', 'c', 'd', 'e', 'f']
    >>> apply_perm(A, [2, 3, 1, 6, 5, 4])
    >>> A
    ['c', 'a', 'b', 'f', 'e', 'd']
    """
    N = len(P)
    for i in range(N):
        if P[i] >= 1:
            # Apply the cycle starting at position i.
            j = i

            last = A[j]
            while P[j] >= 1:
                next = P[j] - 1
                last, A[next] = A[next], last
                P[j] -= N
                j = next

    # Fix P
    for i in range(N):
        P[i] += N

def next_permutation_with_duplicates(A):
    """
    >>> next_permutation_with_duplicates([1, 3, 5, 4, 2])
    [1, 4, 2, 3, 5]
    >>> next_permutation_with_duplicates([1, 1, 1, 2, 2])
    [1, 1, 2, 1, 2]
    >>> next_permutation_with_duplicates([1, 1, 2, 1, 2])
    [1, 1, 2, 2, 1]
    """
    # Copy A into a new array.
    A = A[::]

    N = len(A)
    i = N - 2
    while i >= 0 and A[i] >= A[i+1]:
        i -= 1
    if i < 0:
        return None

    j = N - 1
    while A[j] <= A[i]:
        j -= 1
    # Now A[j] > A[i].
    A[i], A[j] = A[j], A[i]

    # Reverse A[i+1:].
    j = i+1
    while j < N - j + i:
        A[j], A[N-j+i] = A[N-j+i], A[j]
        j += 1

    return A

A = [1, 2, 2, 4, 5]
while A is not None:
    print A
    A = next_permutation_with_duplicates(A)

def next_combination(A, N):
    K = len(A)
    S = set(A)
    for i in reversed(range(1, N+1)):
        if i not in S:
            A.append(i)

    i = K - 1
    while i >= 0:
        if i+1 < len(A) and A[i] < A[i+1]:
            break
        else:
            i -= 1
    if i < 0:
        # Found last combination
        return False

    for j in range(len(A)-1, i, -1):
        if A[j] > A[i]:
            break
    A[i], A[j] = A[j], A[i]

    # Reverse A[i+1:] and truncate to K.
    j = i+1
    while 2 * j < len(A) + i:
        jp = len(A) - (j-i)
        A[j], A[jp] = A[jp], A[j]
        j += 1
    while len(A) > K:
        A.pop()
    return True

def next_combination2(A, N):
    missing = list(set(range(1, N+1)) - set(A))
    missing.sort()

    i = len(A) - 1
    while i >= 0:
        if missing and A[i] < missing[-1]:
            break
        else:
            # A[i] > missing[-1], so missing + [A] is still sorted
            missing.append(A[i])
            i -= 1
    if i < 0:
        # Found last combination
        return False
    for j in range(len(missing)):
        if missing[j] > A[i]:
            break
    missing[j], A[i] = A[i], missing[j]
    for j in range(i+1, len(A)):
        A[j] = missing[j-i-1]
    return True

A = [1, 2, 3]
print A
while next_combination(A, 4):
    print A

import doctest
doctest.testmod()

