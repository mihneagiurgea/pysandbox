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


class DurationInTraffic(NamedTuple):
    best_guess: str
    pessimistic: str
    optimistic: str


class RouteTraffic(NamedTuple):
    summary: str
    distance: str
    duration: DurationInTraffic


class TrafficSummary(NamedTuple):
    origin: str
    destination: str
    departure_time: datetime.datetime
    routes: List[RouteTraffic]


class CachedCli(object):
    def __init__(self, filename="cache.pickle", key=API_KEY):
        self.cache = Cache(filename)
        self.gmaps = googlemaps.Client(key=key)

    def traffic_summary(
        self, origin: str, destination: str, departure_time: datetime.datetime
    ) -> TrafficSummary:
        # TODO - implement me based on summarize
        # https://developers.google.com/maps/documentation/directions/overview#Routes
        pass

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
