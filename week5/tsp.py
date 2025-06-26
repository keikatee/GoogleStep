#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return solve_opt2(tour, cities)


def solve_opt2(tour: list[int], cities: list[tuple[float, float]]) -> list[int]:
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour) - 1):
                a, b = tour[i - 1], tour[i]
                c, d = tour[j], tour[j + 1]

                # 距離が短くなるならば、辺 (a-b) と (c-d) を (a-c)+(b-d) に入れ替える
                if (distance(cities[a], cities[b]) + distance(cities[c], cities[d])
                        > distance(cities[a], cities[c]) + distance(cities[b], cities[d])):
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improved = True
    return tour
