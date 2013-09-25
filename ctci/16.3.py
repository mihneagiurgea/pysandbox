import time
import threading


class Philosopher(object):

    def __init__(self, left_fork, right_fork, i):
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.hungry = True
        self.i = i

    def run(self):
        print 'Philosopher #%d is hungry' % self.i
        while self.hungry:
            self.try_eat()
            time.sleep(0.1)

    def try_eat(self):
        if self.left_fork.locked() or self.right_fork.locked():
            return

        self.left_fork.acquire()
        acquired = self.right_fork.acquire(False)
        if acquired:
            self.feed()
            self.right_fork.release()

        self.left_fork.release()

    def feed(self):
        print 'Philosopher #%d is feeding...' % self.i
        time.sleep(0.2)
        self.hungry = False
        print 'Philosopher #%d is done feeding.' % self.i


def philosophers(N=5):
    forks = [threading.Lock() for i in xrange(N)]
    philosophers = [
        Philosopher(forks[i], forks[(i+1) % N], i)
        for i in xrange(N)
    ]
    threads = [
        threading.Thread(target=philosophers[i].run)
        for i in xrange(N)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    philosophers(5)
