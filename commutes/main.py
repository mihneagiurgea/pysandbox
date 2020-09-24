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

# results["pessimistic"] = gmaps.directions(
#     origin,
#     destination,
#     mode="driving",
#     alternatives=True,
#     departure_time=departure_time,
#     traffic_model="pessimistic",
# )


# results["pessimistic"] = gmaps.directions(
#     origin,
#     destination,
#     mode="driving",
#     alternatives=True,
#     departure_time=arrive_by,
#     traffic_model="pessimistic",
# )

# gmaps = googlemaps.Client(key=API_KEY)

# # Geocoding an address
# geocode_result = gmaps.geocode("1600 Amphitheatre Parkway, Mountain View, CA")
# print(geocode_result)

# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# print(reverse_geocode_result)

# # Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions(
#     "Sydney Town Hall", "Parramatta, NSW", mode="transit", departure_time=now
# )
# print(directions_result)
