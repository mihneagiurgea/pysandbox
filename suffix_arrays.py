from radix_sort import count_sort

def compute_suffix_arrays(string):
    N = len(string)

    # Each suffix is identified by its starting position in the initial string.
    ordered_suffixes = range(N)

    # Initially, sort each suffix using the 1st character; do this by
    # assigning a value to each suffix = ord(1st character).
    key = [ord(char) for char in string]
    # Extend the key array with N "0"-s, for easier suffix comparison.
    key.extend([0] * N)

    temp = [0] * N

    step = 1
    while step <= N:
        # Re-sort the suffixes, looking at the first 2*step characters;
        # the new key for each suffix becomes (key[i], key[i+step]), so
        # we'll just use a 2-step radix-sort.
        count_sort(ordered_suffixes, key=lambda i: key[i+step])
        count_sort(ordered_suffixes, key=lambda i: key[i])

        # Compute the new key (in a separate array).
        # The value of the smalles suffix is 1.
        temp[ordered_suffixes[0]] = last = 1
        for i in xrange(1, N):
            crnt = ordered_suffixes[i]
            prev = ordered_suffixes[i-1]
            # The value of the next smallest suffix is equal to
            # the last value +1 or +0.
            if key[crnt] > key[prev] or key[crnt+step] > key[prev+step]:
                last += 1
            temp[ordered_suffixes[i]] = last
        # key := temp
        for i in xrange(N):
            key[i] = temp[i]

        step *= 2

    return ordered_suffixes

if __name__ == '__main__':
    import time

    N = 10

    pattern = 'assassiniiibaxbaxceifacebaxxulqwertyuioplkjhgfdsaxcvbnmzqazxs' \
              'edcvfrtgvbhyhnmjujmkiolopmississippi'
    string = pattern * (N / len(pattern)) + pattern[:(N % len(pattern))]

    start_time = time.time()
    ordered_suffixes = compute_suffix_arrays(string)
    duration = time.time() - start_time
    print 'Took %.4f seconds' % duration

    if len(string) < 20:
        print ordered_suffixes
        for idx, suffix in enumerate(ordered_suffixes):
            print '%2d) %s' % (idx+1, string[suffix:])