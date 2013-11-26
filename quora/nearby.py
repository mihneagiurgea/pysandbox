from collections import defaultdict, namedtuple
from math import sqrt
import sys

Point = namedtuple('Point', ['x', 'y', 'i'])

def dist_sq(p1, p2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2

class Plane(object):

    MAX_X = 1000000.0

    def __init__(self, points):
        self.N = len(points)

        self.max_x = self.max_y = self.MAX_X
        size = max(self.max_x, self.max_y)
        self.region_size = int(size) / int(sqrt(len(points)))
        # In practice keeping around 6 points per region is faster.
        self.region_size *= 6

        self._cache = {}
        self._regions = defaultdict(list)
        for pt in points:
            self._regions[self.pt_to_region(pt)].append(pt)

    def pt_to_region(self, pt):
        return (int(pt.x) / self.region_size, int(pt.y) / self.region_size)

    def _concentric_squares(self, l):
        if l not in self._cache:
            square = []
            for i in range(2*l+1):
                square.append((-l, -l+i))
                square.append((+l, -l+i))
            for i in range(1, 2*l):
                square.append((-l+i, -l))
                square.append((-l+i, +l))
            self._cache[l] = square
        return self._cache[l]

    def query(self, k, x, y):
        """Return the closest k points to (x, y)."""
        # We can't return more than all results.
        k = min(k, self.N)

        pt = Point(x, y, -1)
        r0 = self.pt_to_region(Point(x, y, -1))
        results = []
        if r0 in self._regions:
            results.extend(self._regions[r0])
        # Add each concentric square around r0, until we have enough results.
        # TODO - explain when we have enough.
        l = 0
        l_target = -1
        while True:
            l += 1
            square = self._concentric_squares(l)
            for ri in square:
                r = (r0[0] + ri[0], r0[1] + ri[1])
                if r in self._regions:
                    results.extend(self._regions[r])
            if l_target == -1:
                if len(results) >= k:
                    l_target = l + (l+1) / 2
            else:
                if l == l_target:
                    break

        # Sort results by distance to pt.
        results.sort(key=lambda p: (dist_sq(pt, p), -p.i))
        return results[:k]


class Solver(object):

    # "Number of topics associated with a question is not more than 10."
    MAX_TOPICS_PER_QUESTION = 10

    def __init__(self, f):
        self.f = f
        T, Q, self.N = map(int, f.readline().split())

        # Read topics and questions.
        topics = []
        for _ in range(T):
            i, x, y = f.readline().split()
            topics.append(Point(float(x), float(y), int(i)))

        self.topic_to_questions = defaultdict(list)
        for _ in range(Q):
            strarr = map(int, f.readline().split())
            question_id = strarr[0]
            for topic_id in strarr[2:]:
                self.topic_to_questions[topic_id].append(question_id)

        # Sort topic_to_questions[topic_id] in descending question_id order,
        # for easier querying.
        for topic_id in self.topic_to_questions:
            self.topic_to_questions[topic_id].sort(reverse=True)

        # Arrange topics in 2D plane.
        self.plane = Plane(topics)

    def solve(self):
        # Answer each query.
        for _ in range(self.N):
            strarr = self.f.readline().split()
            k = int(strarr[1])
            x = float(strarr[2])
            y = float(strarr[3])
            if strarr[0] == 't':
                answer = self.get_closest_topics(k, x, y)
            else:
                answer = self.get_closest_questions(k, x, y)
            print ' '.join(map(str, answer))

    def get_closest_topics(self, k, x, y):
        """Return the k closest topic ids."""
        topics = self.plane.query(k, x, y)
        return [t.i for t in topics]

    def get_closest_questions(self, k, x, y):
        """Return the k closest question ids."""
        k_topics = k * self.MAX_TOPICS_PER_QUESTION
        closest_topic_ids = self.get_closest_topics(k_topics, x, y)

        answer = []
        selected_questions = set()
        for topic_id in closest_topic_ids :
            for question_id in self.topic_to_questions[topic_id]:
                if question_id not in selected_questions:
                    selected_questions.add(question_id)
                    answer.append(question_id)
        return answer[:k]

if __name__ == '__main__':
    f = open('nearby.in', 'r')
    # f = sys.stdin
    solver = Solver(f)
    solver.solve()
