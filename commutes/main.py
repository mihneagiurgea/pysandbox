from typing import List

import googlemaps
import datetime

from cached_cli import CachedCli


def summarize(results):
    print("%d results:" % (len(results)))
    # print(results)
    for result in results:
        legs = result["legs"]
        if len(legs) == 1:
            print("\t%s:" % (result["summary"],))
        else:
            print("\t%s - %d legs:" % (result["summary"], len(legs)))
        for leg in legs:
            print(
                "\t\t Distance: %s Duration: %s Duration in traffic: %s"
                % (
                    leg["distance"]["text"],
                    leg["duration"]["text"],
                    leg["duration_in_traffic"]["text"],
                )
            )


class HomeAnalyzer(object):

    OFFICE_LOCATIONS = [
        "Facebook, 181 Fremont St, San Francisco, CA 94105",
        # The other Facebook
        "Facebook, 1 Hacker Way, Menlo Park, CA 94025",
        "Airbnb HQ, 888 Brannan St, San Francisco, CA 94103",
        "333 Brannan St, San Francisco, CA 94107",
    ]
    DEPARTURE_TIMES = [
        "8:00",
        "8:15",
        "8:30",
        "8:45",
        "9:00",
        "9:15",
        "9:30",
        "9:45",
        "10:00",
        "10:15",
        "10:30",
        "10:45",
        "11:00",
    ]

    def __init__(self, cli: CachedCli):
        self.cli = cli
        self.morning_times = []
        self.evening_times = []
        for s in HomeAnalyzer.DEPARTURE_TIMES:
            hour, minute = s.split(":")
            dt = datetime.datetime(2020, 10, 1, int(hour), int(minute))
            self.morning_times.append(dt)
            dt = dt + datetime.timedelta(hours=8)
            self.evening_times.append(dt)

    def analyze_home(self, origin: str):
        # TODO - write traffic summary for a given location (origin):
        # (1) for each destination in a short list of 3-4
        # (2) commute to office and back
        # (3) assuming 3-5 departure times, and staying 7-9h in the office
        for destination in self.OFFICE_LOCATIONS:
            print("\n\tWork Destination: %s" % destination)
            # Home -> Office
            print(
                "\nMORNING >> Origin: %s -> Destination: %s\n" % (origin, destination)
            )
            self.analyze_one_way(origin, destination, self.morning_times)

            print(
                "\nEVENING >> Origin: %s -> Destination: %s\n" % (destination, origin)
            )
            # Office -> Home
            self.analyze_one_way(destination, origin, self.evening_times)

    def analyze_one_way(
        self, origin: str, destination: str, departure_times: List[datetime.datetime]
    ):
        for departure_time in departure_times:
            summary = self.cli.traffic_summary(origin, destination, departure_time)
            durations = [
                "%s - %s" % (r.duration_optimistic, r.duration_pessimistic)
                for r in summary.routes.values()
            ]
            # print(summary)
            # routes_str = "\n\t".join(map(repr, list(summary.routes.values())))
            print(
                "\tDepart at %s => %s"
                % (summary.departure_time.strftime("%H:%M %p"), " / ".join(durations))
            )


cli = CachedCli()

# origin = "139 Marietta Dr, San Francisco, CA 94127"
origin = "66 Collins St, San Francisco, CA 94118"

# destination = "Facebook, 181 Fremont St, San Francisco, CA 94105"
# departure_time = datetime.datetime(2020, 10, 1, 9, 45)
# results = cli.directions(
#     origin, destination, departure_time, traffic_model="pessimistic"
# )
# summarize(results)
# results = cli.directions(
#     origin, destination, departure_time, traffic_model="optimistic"
# )
# summarize(results)
# results = cli.directions(
#     origin, destination, departure_time, traffic_model="best_guess"
# )
# summarize(results)

# print(cli.traffic_summary(origin, destination, departure_time))

analyzer = HomeAnalyzer(cli)
analyzer.analyze_home(origin)
