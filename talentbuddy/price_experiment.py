import math

def make_f(A, B):
    return lambda x: 0.5 * ( math.sqrt(-3 * x * x + A * x + B) - x - 1 )

def solutions_2nd_degree(a, b, c):
    """Returns the two solutions to ax^2 + bx + c = 0."""
    delta = b * b - 4 * a * c
    sqrt_delta = math.sqrt(delta)
    x1 = (-b - sqrt_delta) / (2 * a)
    x2 = (-b + sqrt_delta) / (2 * a)
    return (x1, x2)

def find_max(f, L, U, epsilon=0.001):
    """Find maximum valud of f(x), for L <= x < U."""
    while L + epsilon < U:
        third = (U - L) / 3
        a = L + third
        b = a + third
        if f(a) < f(b):
            L = a
        else:
            U = b
    return L

def uber_price(a, b):
    # Write your code here
    # To print results to the standard output you can use print
    # Example: print "Hello world!"
    f = make_f(a, b)

    # Solve f(x) = 0
    x1, x2 = solutions_2nd_degree(4, 2-a, 1-b)

    x_max = find_max(f, x1, x2)
    print '%.2f' % x_max
