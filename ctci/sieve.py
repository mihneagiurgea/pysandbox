class Sieve(dict):

    ignored_primes = (2, 3, 5, 7)

    def __getitem__(self, key):
        for prime in self.ignored_primes:
            if key == prime:
                return True
            elif key % prime == 0:
                return False
        print 'Getting %r' % key
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        for prime in self.ignored_primes:
            if key % prime == 0:
                return
        print 'Setting %r to %r' % (key, value)
        return dict.__setitem__(self, key, value)

sieve = Sieve()
print sieve
sieve[2] = 1
sieve[3] = 1
sieve[4] = 0
print sieve
sieve[23*17] = False
print sieve[23*17]