"""
After some 2nd degree equations, we'll come to the following:

(1) N = ( 1 + sqrt( 1 + 8*B*(B-1) ) ) / 2

(2) 1 + sqrt( 1 + 8*B*(B-1) ) = (2K+1)**2 | K integer > 0

(3) B = ( 1 + sqrt( K**2 + (K+1)**2 ) ) / 2

(4) N = K + 1
"""

from pythagorean_triples import iter_pythagorean_triples

def prob(B, N):
    return float(B) * float(B-1) / float(N-1) / float(N)

LOWER_BOUND = 10 ** 12

for triple in iter_pythagorean_triples():
    if triple[0] + 1 != triple[1]:
        continue

    print triple
    K = triple[0]
    N = K + 1
    if (1 + triple[2]) % 2 == 0:
        B = (1 + triple[2]) / 2
        print 'Found N = %d and B = %d (prob = %.6f)' % (N, B, prob(B, N))
        if N >= LOWER_BOUND:
            break
