import random


class Generator(object):

    def __init__(self, filename, T, Q, N,
                 max_x=1000000.0, max_y=1000000.0):
        self.filename = filename

        self.T = T
        self.Q = Q
        self.N = N
        self.max_x = max_x
        self.max_y = max_y

    def generate(self):
        self.f = open(self.filename, 'w')
        self.f.write('%d %d %d\n' % (self.T, self.Q, self.N))
        self._generate_topics()
        self._generate_questions()
        self._generate_queries()
        self.f.close()
        self.f = None

    def _generate_topics(self):
        self.topics = range(self.T)
        for i in range(self.T):
            x = random.random() * self.max_x
            y = random.random() * self.max_y
            self.f.write('%d %.1f %.1f\n' % (i, x, y))

    def _generate_questions(self):
        for i in range(self.Q):
            t = random.randint(0, 10)
            question_topics = random.sample(self.topics, t)
            s = ' '.join(map(str, question_topics))
            self.f.write('%d %d %s\n' % (i, t, s))

    def _generate_queries(self):
        for i in range(self.N):
            k = random.randint(1, 100)
            t = 't' if i % 2 == 0 else 'q'
            x = random.random() * 2.0 * self.max_x
            y = random.random() * 2.0 * self.max_y
            self.f.write('%c %d %.1f %.1f\n' % (t, k, x, y))

if __name__ == '__main__':
    import sys
    T, Q, N = map(int, sys.argv[1:4])
    generator = Generator('nearby.in', T, Q, N)
    generator.generate()