import time
import os
import sys
from Queue import Queue
from threading import Lock, Thread

from socket import *

def pingit(host, port):                               # defining function for later use
    s = socket(AF_INET, SOCK_STREAM)         # Creates socket

    try:
        s.connect((host, port))    # tries to connect to the host
    except ConnectionRefusedError: # if failed to connect
        print("Server offline")    # it prints that server is offline
        s.close()                  #closes socket, so it can be re-used
        pingit()                   # restarts whole process

    s.close()                  # closes socket just in case

RUN_DURATION = 5.0
# 8.3MB
FILEPATH = '/Users/skip/Movies/Cedry2k-CuvinteCeVindeca-2010-SPRiTE/14-cedry2k-actiune_de_noapte-sprite.mp3'
DIR = '/Users/skip/Movies/Cedry2k-CuvinteCeVindeca-2010-SPRiTE/'
HOSTNAME = '10.0.0.1' # 'google.com'
# max throughput = 3.4GBps
KB = 1024
MB = 1024 * KB

lock = Lock()

def work():
    # os.urandom(20 * KB)

    with lock:
        hostname = HOSTNAME
    pingit(hostname, 80)

    # f = open(FILEPATH, 'r')
    # f.seek(6 * MB)
    # content = f.read(6 * KB)
    # content = .read()


    # dirpath = DIR
    # files = os.listdir(dirpath)
    # for filename in files:
    #     path = os.path.join(dirpath, filename)
    #     # os.lstat(path)
    #     f = open(path, 'r')
    #     f.seek(47 * KB)
    #     f.read(2 * KB)


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""

    def __init__(self):
        Thread.__init__(self)
        self.count = 0
        self.running = True

    def run(self):
        time.sleep(0.1)
        start_time = time.time()
        # print 'Started at %.3f' % start_time
        while self.running:
            work()
            self.count += 1
        duration = time.time() - start_time
        # print 'Finished %d tasks in %.3fs' % (self.count, duration)


if __name__ == '__main__':
    num_threads = int(sys.argv[1])

    start_time = time.time()
    threads = []
    for i in range(num_threads):
        t = Worker()
        t.start()
        threads.append(t)

    time.sleep(RUN_DURATION)
    for t in threads:
        t.running = False

    count = 0
    for t in threads:
        t.join()
        count += t.count

    duration = time.time() - start_time
    # print 'Joined all %d threads in %.3fs' % (num_threads, duration)
    print 'Completed %d tasks in %.3fs' % (count, duration)
    print 'RPS: %.2f' % (float(count) / duration, )
