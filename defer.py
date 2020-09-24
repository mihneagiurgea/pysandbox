from threading import *
import time, threading, os
import random
from heapq import heappush as push
from heapq import heappop as pop
# from multiprocessing import Pool
from multiprocessing.pool import ThreadPool, Pool

# Defer problem
min_heap = []
cv = threading.Condition()

def f(ts):
    # 3 / 0
    print "[%s] I should be executed at time [%d]. I am executing at time [%f]" % (os.getpid(), ts, time.time())
    time.sleep(random.random() * 3)

pool = Pool(5)

def producer():
    for ts in range(10, 0, -2):

        with cv:
            push(min_heap, time.time() + ts)
            cv.notify()

def consumer():
    while True:

        with cv:
            while not min_heap:
                cv.wait()

            ts = min_heap[0]

            if ts < time.time():
                ts = pop(min_heap)
                r = pool.apply_async(f, args=(ts, ))
                print r
                # print r, r.ready()
                # print r.wait(), r.get()
                # print r.successful()



            else:
                print "Fuck this, I'm going to sleep...."
                cv.wait(ts - time.time())


p = threading.Thread(target = producer)
c = threading.Thread(target = consumer)

p.start()
c.start()

p.join()
c.join()
