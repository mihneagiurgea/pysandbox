import datetime
from typing import Dict, List, NamedTuple

import googlemaps

from cache import Cache
from settings import API_KEY


class DirectionsRequest(NamedTuple):
    origin: str
    destination: str
    departure_time: datetime.datetime
    traffic_model: str


class RouteTraffic(object):
    summary: str
    distance: str
    duration_pessimistic: str
    duration_optimistic: str

    def __init__(self, summary, distance):
        self.summary = summary
        self.distance = distance
        self.duration_pessimistic = None
        self.duration_optimistic = None

    def __repr__(self):
        return "[%s] Distance: %s Duration: %s - %s" % (
            self.summary,
            self.distance,
            self.duration_optimistic,
            self.duration_pessimistic,
        )


class TrafficSummary(NamedTuple):
    origin: str
    destination: str
    departure_time: datetime.datetime
    routes: Dict[str, RouteTraffic]

    def __repr__(self):
        routes_str = "\n\t\t".join(map(repr, list(self.routes.values())))
        return "TrafficSummary(origin: %s -> destination: %s):\n\tdeparture_time: %s\troutes:\n\t\t%s" % (
            self.origin,
            self.destination,
            self.departure_time.strftime("%c"),
            routes_str,
        )


class CachedCli(object):
    def __init__(self, filename="cache.pickle", key=API_KEY):
        self.cache = Cache(filename)
        self.gmaps = googlemaps.Client(key=key)

    def traffic_summary(
        self, origin: str, destination: str, departure_time: datetime.datetime
    ) -> TrafficSummary:
        routes = {}  # type: Dict[str, RouteTraffic]
        # https://developers.google.com/maps/documentation/directions/overview#Routes
        for traffic_model in ("optimistic", "pessimistic"):
            results = self.directions(
                origin=origin,
                destination=destination,
                departure_time=departure_time,
                traffic_model=traffic_model,
            )
            for result in results:
                summary = result["summary"]

                legs = result["legs"]
                assert len(legs) == 1
                leg = legs[0]

                distance = leg["distance"]["text"]
                duration = leg["duration_in_traffic"]["text"]

                # Add to routes
                if summary not in routes:
                    routes[summary] = RouteTraffic(summary=summary, distance=distance)
                if traffic_model == "optimistic":
                    routes[summary].duration_optimistic = duration
                else:
                    routes[summary].duration_pessimistic = duration

        return TrafficSummary(
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            routes=routes,
        )

    def directions(
        self,
        origin: str,
        destination: str,
        departure_time: datetime.datetime,
        traffic_model="pessimistic",
    ) -> dict:
        request = DirectionsRequest(
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            traffic_model=traffic_model,
        )
        return self._get(request)

    def _get(self, request: DirectionsRequest):
        return self.cache.get(request, self._fetch)

    def _fetch(self, request: DirectionsRequest):
        return self.gmaps.directions(
            request.origin,
            request.destination,
            mode="driving",
            alternatives=True,
            departure_time=request.departure_time,
            traffic_model=request.traffic_model,
        )
