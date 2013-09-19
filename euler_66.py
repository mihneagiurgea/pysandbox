import math

MAX_Y = 200000
MAX_D = 100

squares = [ i ** 2 for i in xrange(MAX_Y+1) ]
squares_set = set(squares)

# D = 0
values = [1] * MAX_Y

for D in xrange(1, MAX_D):
    for i in xrange(1, MAX_Y):
        values[i] += squares[i]

    if D in squares_set:
        # No solutions when D is square.
        continue

    min_x = None
    for i in xrange(1, MAX_Y):
        if values[i] in squares_set:
            min_x = math.sqrt(values[i])
            break

    if min_x is None:
        print 'No solution found for D=%d' % D
        break
    else:
        print 'Sol(D=%d) = %d' % (D, min_x)

