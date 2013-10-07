import Queue as queue
import time
from threading import Thread

class WorkerThread(Thread):

    def __init__(self, work_queue):
        Thread.__init__(self)
        self.work_queue = work_queue
        self.running = True
        self.terminated = False

    def run(self):
        while self.running:
            request = self._get_request()
            if request:
                self._handle_request(request)

        # Complete all remaining tasks, then exit.
        while not self.terminated:
            request = self._get_request(False)
            if request:
                self._handle_request(request)
            else:
                break

    def _get_request(self, timeout=0.1):
        try:
            block = True if timeout else False
            return self.work_queue.get(block, timeout)
        except queue.Empty:
            return None

    def close(self):
        self.running = False

    def terminate(self):
        self.running = False
        self.terminated = True

    def _handle_request(self, request):
        func, args, kwargs, callback = request
        result = func(*args, **kwargs)
        if callback:
            callback(result)
        self.work_queue.task_done()


class ThreadPool(Thread):

    def __init__(self, max_threads=10):
        Thread.__init__(self)
        self.max_threads = max_threads
        self.threads = []
        self.work_queue = queue.Queue()
        self.running = True
        self.terminated = False

    def run(self):
        self._start_workers()
        while self.running:
            time.sleep(0.1)

        # Wait for all worker threads to exit.
        if not self.terminated:
            self.work_queue.join()
        for thread in self.threads:
            thread.join()

    def close(self):
        self.running = False
        for thread in self.threads:
            thread.close()

    def terminate(self):
        self.running = False
        self.terminated = True
        for thread in self.threads:
            thread.terminate()

    def apply_async(self, func, args=None, kwargs=None, callback=None):
        request = (func, args or (), kwargs or {}, callback)
        self.work_queue.put(request)

    def _start_workers(self):
        for i in range(self.max_threads):
            thread = WorkerThread(self.work_queue)
            thread.start()
            self.threads.append(thread)


def test_thread_pool():

    results = []
    def callback(result):
        results.append(result)
        # print 'callback(%r)' % (result, )

    def f(i):
        time.sleep((i % 9) * 0.1)
        return i

    N = 30

    pool = ThreadPool(30)
    pool.start()
    for i in range(1, N):
        pool.apply_async(f, args=(i, ), callback=callback)
        time.sleep(0.01)

    time.sleep(0.1)

    print 'Closing pool & joining...'
    pool.terminate()
    pool.join()
    print 'Closed pool.'

    print 'len(results) = %d/%d' % (len(results), N)

if __name__ == '__main__':
    test_thread_pool()







