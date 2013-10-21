from collections import defaultdict
from heapq import heappush, heappop

def build_graph(city_map):
    graph = defaultdict(list)
    for edge in city_map:
        i, j, w = map(int, edge.split(','))
        graph[i].append((j, w))
        graph[j].append((i, w))
    return graph

def dijkstra(graph, start_node):
    distances = {}
    visited = set()

    # A priority queue of (cost, node).
    min_heap = []
    heappush(min_heap, (0, start_node))

    distances[start_node] = 0
    while len(visited) < len(graph) and min_heap:
        # Extract node with minimum weight.
        node = heappop(min_heap)[1]
        while node in visited:
            node = heappop(min_heap)[1]

        visited.add(node)

        for i, w in graph[node]:
            if i not in distances or distances[i] > distances[node] + w:
                distances[i] = distances[node] + w
                heappush(min_heap, (distances[i], i))
    return distances

def find_closest_car(city_map, cars, customer):
    graph = build_graph(city_map)
    distances = dijkstra(graph, customer)
    # Find closest car
    closest_car = 0
    for i in range(1, len(cars)):
        if distances[cars[i]] < distances[cars[closest_car]]:
            closest_car = i
    print closest_car + 1