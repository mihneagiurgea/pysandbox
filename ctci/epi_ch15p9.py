import threading
import time

NR_CHAIRS = 4

lock = threading.Lock()
waiting_customers = threading.Condition(threading.Semaphore(0))
active_customers = threading.Semaphore(0)

class Barber(threading.Thread):

    def __init__(self, lock, waiting_customers, active_customers):
        self.lock = lock
        self.waiting_customers = waiting_customers
        self.active_customers = active_customers
        self.sleeping = None

    def run(self):
        while True:
            # Barber is sleeping.
            with self.lock:
                self.sleeping = True
            self.waiting_customers.wait()

            # Change state to cutting hair.
            with self.lock:
                self.sleeping = False
            self.active_customers.release()

            print 'Barber is working...'
            time.sleep(0.3)


class Customer(threading.Thread):

    def __init__(self, barber, i):
        self.barber = barber
        self.lock = barber.lock
        self.waiting_customers = barber.waiting_customers
        self.active_customers = barber.active_customers
        self.i = i

    def __str__(self):
        return 'Customer #%d' % self.i

    def run(self):
        print '%s is entering the store...'

        self.lock.acquire()
        if self.barber.sleeping:
            self.lock.release()
            # Increment number of waiting customers.
            self.waiting_customers.release()
            # Sit on the barber chair.
            print '%s is getting his hair cut...'
            self.active_customers.acquire()

            self.waiting_customers.acquire()
            print '%s is leaving...'
        else:
            self.lock.release()
            print '%s is waiting...'
            self.waiting_customers.release()





