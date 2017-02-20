from collections import defaultdict
from itertools import product
import random

def read_dataset(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    rows = [tuple(line.strip().split('|')) for line in lines]
    return rows

def unpack_row(row):
    dims = [ d.split(',') for d in row ]
    return list(product(*dims))

def unpack_all_rows_and_normalize(rows):
    results = []
    for row in rows:
        results.extend(unpack_row(row))
    unique = set(results)
    return sorted(list(unique))

def are_equivalent(A, B, virtualA=None, virtualB=None):
    if virtualA:
        A = A[:]
        A.extend(virtualA)
    if virtualB:
        B = B[:]
        B.extend(virtualB)
    rows_A = unpack_all_rows_and_normalize(A)
    rows_B = unpack_all_rows_and_normalize(B)
    return rows_A == rows_B

def compress_dimention(rows, d):
    grouping = defaultdict(set)
    for row in rows:
        row_without_d = row[:d] + row[d+1:]
        grouping[row_without_d].update(row[d].split(','))

    compressed_rows = []
    for row_without_d, values_set in grouping.iteritems():
        # Is this sorted necessary?
        sorted_values = sorted(list(values_set))
        values_string = ','.join(sorted_values)
        row = row_without_d[:d] + (values_string, ) + row_without_d[d:]
        compressed_rows.append(row)
    return compressed_rows

def compress_all_rows(rows):
    N = len(rows[0])
    for d in range(N):
        rows = compress_dimention(rows, d)
    return rows

def print_2D(normalized_rows):
    points = set()
    for row in normalized_rows:
        p = (int(row[0]), int(row[1]))
        points.add(p)

    printed = 0
    for i in range(1, 31):
        line = ''
        for j in range(1, 31):
            if (i, j) in points:
                line += 'X '
                printed += 1
            else:
                line += '  '
        print line
    assert printed == len(normalized_rows)

def print_filename(f):
    rows = read_dataset(f)
    rows = unpack_all_rows_and_normalize(rows)
    print '===%s===' % f
    print_2D(rows)

def check(f1, f2):
    rows1 = read_dataset(f1)
    rows2 = read_dataset(f2)
    if are_equivalent(rows1, rows2):
        print 'Ok. rows(%s) = rows(%s)' % (f1, f2)
    else:
        print 'Wrong! rows(%s) != rows(%s)' % (f1, f2)
        print_filename(f1)
        print_filename(f2)

def backtrack(dims, k, A, results):
    if k == len(dims):
        results.append(tuple(A))
        return
    for i in range(0, len(dims[k])):
        A[k] = dims[k][i]
        backtrack(dims, k+1, A, results)

def get_all_points_set(rows):
    D = len(rows[0])
    dims = [set() for _ in range(D)]
    for row in rows:
        for d in range(D):
            x = row[d]
            x.split(',')
            dims[d].update(x.split(','))

    # dims[0] = set(['a0', 'a1', 'a2'])
    # dims[1] = set(['b0', 'b1', 'b2'])
    dims[2] = set([''])
    dims[3] = set(['d3'])
    dims[4] = set([''])

    # Convert to list of lists.
    dims = [ tuple(x) for x in dims ]
    print 'Dims: %s' % dims

    results = []
    A = [''] * D
    backtrack(dims, 0, A, results)

    # Remove points already there.
    set_of_rows = set(rows)
    results = [p for p in results if p not in set_of_rows]

    print 'Found a total of %d potential virtual rows:' % len(results)
    # print '%s...' % results[:5]

    return results

def compress(rows):
    rows = unpack_all_rows_and_normalize(rows)
    print 'Unpacked to %d rows' % len(rows)

    # Mandatory virtual.
    pt0 = ('a0', 'b0', 'c0', 'd0', 'e0')
    rows.append(pt0)

    potential = get_all_points_set(rows)

    virtual = [pt0]
    solution = compress_all_rows(compress_all_rows(rows))

    for pt in potential:
        rows.append(pt)

        compressed_rows = compress_all_rows(rows)
        if len(compressed_rows) < len(solution):
            solution = compressed_rows
            virtual = [pt0, pt]

        rows.pop()

    print 'Solution: %d rows using virtual: %s' % (len(solution), virtual)

    return virtual, solution

def solve(filename):
    input_rows = read_dataset(filename)
    print 'Read %d rows' % len(input_rows)

    virtual, rows = compress(input_rows)

    # Check valid solution
    if not are_equivalent(input_rows, rows, virtual):
        print 'Output rows are NOT equivalent!'

    # Output to console
    rows.sort(key=lambda r: r[0])

    # Output to filename
    output_filename = 'solved-%s' % filename
    f = open(output_filename, 'w')
    if virtual:
        for row in virtual:
            s = '|'.join(row)
            f.write('%s\n' % s)
        f.write('\n')
    for row in rows:
        s = '|'.join(row)
        f.write('%s\n' % s)
    f.close()
    print 'Written output to %s' % output_filename

if __name__ == '__main__':
    filename = 'dataset-003.txt'
    # check(filename, 'optimal-dataset-002.txt')
    solve(filename)
