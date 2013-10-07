import random
import time
from threading import Condition, Thread

class AllRendezvous(object):

    def __init__(self, N):
        self.condition = Condition()
        self.N = N
        self.counter = 0

    def inc(self):
        with self.condition:
            self.counter += 1
            if self.counter == self.N:
                self.condition.notify()

    def is_ok(self):
        with self.condition:
            return self.counter == self.N

    def wait(self):
        with self.condition:
            while not self.is_ok():
                self.condition.wait()

class NextCritical(object):

    def __init__(self, N):
        self.condition = Condition()
        self.N = N
        self.calls = [0] * N
        self.max_calls = 1

    def is_ok(self, i):
        with self.condition:
            # print '%r / %d' % (self.calls, self.max_calls)
            return self.calls[i] < self.max_calls

    def wait(self, i):
        with self.condition:
            while not self.is_ok(i):
                self.condition.wait()

    def inc(self, i):
        with self.condition:
            if self.is_ok(i):
                self.calls[i] += 1
                if sum(self.calls) == self.max_calls * self.N:
                    self.max_calls += 1
                    self.condition.notifyAll()
            else:
                raise RuntimeError('Cannot inc while condition is not met.')


class MyThread(Thread):

    def __init__(self, i, all_rendezvous, next_critical):
        Thread.__init__(self)
        self.i = i
        self.all_rendezvous = all_rendezvous
        self.next_critical = next_critical
        self._called_rendezvous = False

    def __str__(self):
        return 'Thread(%d)' % (self.i+1)

    def run(self):
        self.sleep()
        self.rendezvous()
        self.sleep()
        self.rendezvous()
        self.sleep()
        self.rendezvous()
        for i in range(5):
            self.critical()
            self.sleep()

    def sleep(self):
        time.sleep(random.random())

    def rendezvous(self):
        if not self._called_rendezvous:
            self._called_rendezvous = True
            self.all_rendezvous.inc()

    def critical(self):
        # print '\t%s -> entering .critical()' % self
        self.all_rendezvous.wait()

        # print '\t%s -> all_rendezvous condition was met' % self

        self.next_critical.wait(self.i)
        with self.next_critical.condition:
            print '%s.critical()' % self
            self.next_critical.inc(self.i)

        # with self.next_critical.condition:

        #     # print '\t%s -> checking next_critical condition...' % self

        #     while not self.next_critical.is_ok(self.i):
        #         self.next_critical.condition.wait()
        #     print '%s.critical()' % self
        #     self.next_critical.inc(self.i)

def run_threads(N=3):
    all_rendezvous = AllRendezvous(N)
    next_critical = NextCritical(N)

    threads = []
    for i in range(N):
        thread = MyThread(i, all_rendezvous, next_critical)
        threads.append(thread)

    for thread in threads:
        print 'Starting %s...' % thread
        thread.start()

    for thread in threads:
        thread.join()
        print 'Joined %s' % thread

if __name__ == '__main__':
    run_threads(3)
