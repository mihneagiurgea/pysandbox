from collections import defaultdict, namedtuple

Point = namedtuple('Point', ['x', 'y', 'i'])

def dist_sq(p1, p2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2

class Plane(object):

    def __init__(self, points):
        self.points = points

    def query(self, k, x, y):
        """Return the closest k points to (x, y)."""
        pt = Point(x, y, -1)
        self.points.sort(key=lambda p: (dist_sq(pt, p), -p.i))
        return self.points[:k]


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
    solver = Solver(f)
    solver.solve()
