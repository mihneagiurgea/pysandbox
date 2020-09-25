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


OFFICE_LOCATIONS = [
    "Facebook, 181 Fremont St, San Francisco, CA 94105",
    # Assuming Google is right next to Facebook
    "Airbnb HQ, 888 Brannan St, San Francisco, CA 94103",
    "333 Brannan St, San Francisco, CA 94107",
]
DEPARTURE_TIMES = [
    "8:30",
    "8:45",
    "9:00",
    "9:15",
    "9:30",
    "9:45",
    "10:00",
]


def analyze_home(cli: CachedCli, origin: str):
    # TODO - write traffic summary for a given location (origin):
    # (1) for each destination in a short list of 3-4
    # (2) commute to office and back
    # (3) assuming 3-5 departure times, and staying 7-9h in the office
    for destination in OFFICE_LOCATIONS:
        for s in DEPARTURE_TIMES:
            hour, minute = s.split(":")
            departure_time = datetime.datetime(2020, 10, 1, int(hour), int(minute))
            print(cli.traffic_summary(origin, destination, departure_time))


cli = CachedCli()

origin = "139 Marietta Dr, San Francisco, CA 94127"
destination = "Facebook, 181 Fremont St, San Francisco, CA 94105"
departure_time = datetime.datetime(2020, 10, 1, 9, 45)
results = cli.directions(
    origin, destination, departure_time, traffic_model="pessimistic"
)
summarize(results)
results = cli.directions(
    origin, destination, departure_time, traffic_model="optimistic"
)
summarize(results)
results = cli.directions(
    origin, destination, departure_time, traffic_model="best_guess"
)
summarize(results)

print(cli.traffic_summary(origin, destination, departure_time))

analyze_home(cli, origin)
