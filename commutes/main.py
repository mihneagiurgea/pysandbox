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
        # San Francisco
        "Facebook, 181 Fremont St, San Francisco, CA 94105",
        "Airbnb HQ, 888 Brannan St, San Francisco, CA 94103",
        "333 Brannan St, San Francisco, CA 94107",
        # South Bay
        "Facebook, 1 Hacker Way, Menlo Park, CA 94025",
    ]
    DEPARTURE_TIMES_MORNING = [
        "8:00",
        "8:15",
        "8:30",
        "8:45",
        "9:00",
        "9:15",
        "9:30",
        "9:45",
        "10:00",
    ]
    DEPARTURE_TIMES_EVENING = [
        "16:00",
        "16:30",
        "17:00",
        "17:30",
        "18:00",
        "18:30",
        "19:00",
        "19:30",
        "20:00",
    ]

    def __init__(self, cli: CachedCli):
        self.cli = cli
        self.morning_times = [
            self.convert(t) for t in HomeAnalyzer.DEPARTURE_TIMES_MORNING
        ]
        self.evening_times = [
            self.convert(t) for t in HomeAnalyzer.DEPARTURE_TIMES_EVENING
        ]

    def convert(self, time: str) -> datetime.datetime:
        hour, minute = time.split(":")
        return datetime.datetime(2020, 10, 1, int(hour), int(minute))

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
# origin = "66 Collins St, San Francisco, CA 94118"
# origin = "1447 Funston Ave, San Francisco, CA"
origin = "731 8th Ave, San Francisco, CA"

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
