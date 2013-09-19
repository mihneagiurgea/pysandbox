from collections import defaultdict

HOUR = 100
DAY = 24 * HOUR

class Flight(object):

    def __init__(self, start_time, start_city, dest_city, arrival_time):
        self.start_time = start_time
        self.arrival_time = arrival_time
        self.start_city = start_city
        self.dest_city = dest_city
        # Does the flight arrive in the next day?
        self.next_day = arrival_time <= start_time

    def fly(self, time):
        """Computes the soonest you can arrive in the destination city by
        using this flight and leaving anywhere after time.
        """
        days = time / DAY * DAY
        time_of_day = time % DAY
        # Can we catch this flight today?
        if time_of_day > self.start_time:
            days += DAY
        return days + self.arrival_time + DAY * self.next_day

def solve(timetable, start_city, start_time, dest_city):
    outgoing = defaultdict(list)
    for flight in timetable:
        outgoing[flight.start_city].append(flight)

    # The soonest you can arrive into each city.
    soonest = {}
    # The cities we have visited (optimized) so far.
    visited = set()
    # Add the start_city and start_time.
    soonest[start_city] = start_time - HOUR

    while dest_city not in visited:
        # What is the city we can arrive into earliest, and which we have not
        # visited yet?
        min_city = None
        for city in soonest:
            if city not in visited:
                if min_city is None or soonest[city] < soonest[min_city]:
                    min_city = city

        if min_city is None:
            raise ValueError('No path to %s' %  dest_city)

        # When can we board a flight (add 1 HOUR for transit time).
        min_flight_time = soonest[min_city] + HOUR

        # Add min_city to visited, and expand it.
        visited.add(min_city)
        for flight in outgoing[min_city]:
            if flight.dest_city not in visited:
                arrival_time = flight.fly(min_flight_time)
                # Relax cost to flight.dest_city by using the current flight.
                soonest.setdefault(flight.dest_city, arrival_time)
                soonest[flight.dest_city] = min(soonest[flight.dest_city],
                                                arrival_time)

    return soonest[dest_city]

if __name__ == '__main__':
    timetable = [
        Flight(1000, 'C1', 'C2', 1400),
        Flight(2100, 'C1', 'C2', 0100),
        Flight(1430, 'C2', 'C4', 2030),
        Flight(1230, 'C1', 'C3', 1430),
        Flight(1600, 'C3', 'C4', 1800),
    ]
    print solve(timetable, 'C1', 900, 'C4')