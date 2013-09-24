from heapq import heappop, heappush
import time
import threading


class MaxHeap(object):
    """Wrapper over Python's heapq module, disguised as a max-heap."""

    def __init__(self):
        self.heap = []

    def push(self, value):
        heappush(self.heap, -value)

    def pop(self):
        return -heappop(self.heap)

    def top(self):
        return -self.heap[0]

    def __len__(self):
        return len(self.heap)


class SyncedHistory(object):

    def __init__(self, history):
        self.lock = threading.Lock()
        self.history = history
        self.live_trades = MaxHeap()

    def add(self, value):
        with self.lock:
            self.live_trades.push(value)

    def __len__(self):
        with self.lock:
            return len(self.history) + len(self.live_trades)

    def top(self, t):
        with self.lock:
            # Merge live_trades + history and return top t.
            top = []
            # We need to remember what elements we removed from live_trades,
            # to put them back.
            temp = []
            i = 0
            while len(top) < t:
                # All bids are positive, so we can use "-1" as -INF
                best_history = best_live_trades = -1
                if i < len(self.history):
                    best_history = self.history[i]
                if len(self.live_trades) > 0:
                    best_live_trades = self.live_trades.top()
                if best_history > best_live_trades:
                    i += 1
                    top.append(best_history)
                else:
                    self.live_trades.pop()
                    temp.append(best_live_trades)
                    top.append(best_live_trades)

            # Put back all elements removed from the MaxHeap.
            for v in temp:
                self.live_trades.push(v)

            return top


class StreamReaderThread(threading.Thread):

    def __init__(self, stream, history):
        threading.Thread.__init__(self)
        self.stream = stream
        self.history = history
        self.running = True

    def run(self):
        while self.running:
            line = self.stream.readline().strip()
            if line:
                # print 'Read line: %r' % line
                self.on_new_line(line)
            else:
                time.sleep(0.05)

    def on_new_line(self, line):
        # Override me :)
        pass


class ControlThread(StreamReaderThread):

    def __init__(self, stream, output_stream, history):
        StreamReaderThread.__init__(self, stream, history)
        self.output_stream = output_stream

    def on_new_line(self, line):
        strarr = line.split()

        if len(strarr) == 1:
            # "end" command"
            self.running = False
            return

        # Try to process "top" command, or wait for more data.
        n = int(strarr[1])
        t = int(strarr[2])
        while len(self.history) < n:
            time.sleep(0.05)
        # print 'n = %d len(history) = %d' % (n, len(self.history))
        output = ' '.join(map(str, self.history.top(t)))
        self.output_stream.write('%s\n' % output)
        self.output_stream.flush()


class BidStreamThread(StreamReaderThread):

    def on_new_line(self, line):
        v = int(line)
        self.history.add(v)


def main(f_history, f_control, f_output, f_bid_streams):
    # Process the history file.
    lines = f_history.readlines()
    f_history.close()
    historical_values = map(int, lines[1:])[::-1]

    history = SyncedHistory(historical_values)

    # Start all threads.
    control_thread = ControlThread(f_control, f_output, history)
    control_thread.start()

    bid_stream_threads = []
    for f_bid_stream in f_bid_streams:
        t = BidStreamThread(f_bid_stream, history)
        t.start()
        bid_stream_threads.append(t)

    # Join control thread until it reads an "end", then close all other
    # threads.
    control_thread.join()
    for thread in bid_stream_threads:
        thread.running = False
        thread.join()

if __name__ == '__main__':
    import sys

    # Read file names and create handlers for each.
    f_history = open(sys.argv[1], 'r')
    f_control = open(sys.argv[2], 'r')
    f_output = open(sys.argv[3], 'w')
    f_bid_streams = []
    for i in xrange(4, 8):
        f_bid_streams.append(open(sys.argv[i], 'r'))

    main(f_history, f_control, f_output, f_bid_streams)

    # Close files (at least those we care about).
    f_output.close()
