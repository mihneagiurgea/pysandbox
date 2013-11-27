import copy
from itertools import permutations


def get_all_subsets(S):
    """Given a set S, return all 2^||S|| subsets of S."""
    N = len(S)
    nr_subsets = 2 ** N
    for i in range(nr_subsets):
        subset = []
        for j in range(N):
            if i & (1 << j):
                subset.append(S[j])
        yield subset

def get_all_mappings(R, T):
    """Return all mappings f: R -> T such f is an arbitrary function
    (not necessary injective)."""
    N = len(R)
    M = len(T)
    nr_mappings = M ** N
    for i in range(nr_mappings):
        mapping = {}
        # Interpret i as a N-digit number in base M.
        for j in range(N):
            digit = i % M # between 0..M-1
            mapping[R[j]] = T[digit]
            i /= M
        yield mapping

def get_all_shuffled_mappings(mapping):
    """Given a < <int> -> tuple<Int> > mapping, return all mappings m such that:
      * m.keys() == mapping.keys()
      * set(m[k]) == set(mapping[k])

    TODO - refactor to an iterative implementation
    """
    keys = sorted(mapping.keys())

    def backtracking(m, i, results):
        if i == len(keys):
            results.append(copy.deepcopy(m))
        else:
            key = keys[i]
            for perm in permutations(mapping[key]):
                m[key] = perm
                backtracking(m, i+1, results)

    results = []
    backtracking({}, 0, results)
    return iter(results)
