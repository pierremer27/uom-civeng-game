from queue import PriorityQueue
from collections import deque
import statistics


class Location():
    def __init__(self, x: int, y: int, name: str, color: str):
        self.x = x
        self.y = y
        self.name = name
        self.color = color

    def __eq__(self, other):
        if isinstance(other, Location):
            return self.x == other.x and self.y == other.y and self.name == other.name and self.color == other.color
        return False

    def __str__(self):
        return self.name + " (" + str(self.x) + "," + str(self.y) + ")"


class Connection():
    def __init__(self, a: Location, b: Location):
        self.a = a
        self.b = b
        self.times_used = 0

    def __eq__(self, other):
        if isinstance(other, Connection):
            return (self.a == other.a and self.b == other.b) or (self.a == other.b and self.b == other.a)
        return False

    def __str__(self):
        return str(self.a) + ' <-> ' + str(self.b) + ' (Crossed ' + str(self.times_used) + ' times)'

    def distance(self):
        return ((((self.b.x - self.a.x)**2) + ((self.b.y-self.a.y)**2))**0.5)


class LocationGraph():
    def __init__(self, locations):
        self.locations = locations
        self.connections = []

    def add_connection(self, a: Location, b: Location):
        self.connections.append(Connection(a, b))

    def pathfind(self, start: Location, end: Location):
        start_idx = self.__get_location_index(start)
        end_idx = self.__get_location_index(end)
        open = [start_idx]
        g_score = {}
        f_score = {}
        came_from = {}
        for i in range(len(self.locations)):
            g_score[i] = 2147800000  # Infinity
            f_score[i] = 2147800000  # Infinity
        g_score[start_idx] = 0  # Distance to itself is zero
        f_score[start_idx] = self.__distance(start_idx, end_idx)

        while len(open) > 0:
            current_idx = self.__get_lowest_score_node(open, f_score)
            if current_idx == end_idx:
                return self.__reconstruct_path(came_from, current_idx)
            open = [j for _, j in enumerate(open) if j != current_idx]
            neighbours = self.__get_loc_neighbours(self.locations[current_idx])
            for n in neighbours:
                tentative_g_score = g_score[current_idx] + \
                    self.__distance(current_idx, n)
                if tentative_g_score < g_score[n]:
                    came_from[n] = current_idx
                    g_score[n] = tentative_g_score
                    f_score[n] = tentative_g_score + \
                        self.__distance(n, end_idx)
                    if n not in open:
                        open.append(n)
        return None

    def __reconstruct_path(self, came_from: dict, current):
        nodes = deque()
        nodes.appendleft(current)
        while current in came_from.keys():
            current = came_from[current]
            nodes.appendleft(current)
        connections = []
        for i in range(len(nodes) - 1):
            connections.append(
                self.__get_connection_between(nodes[i], nodes[i + 1]))
            connections[-1].times_used += 1
        return connections

    def __get_connection_between(self, a_idx, b_idx):
        con = None
        for i in range(len(self.connections)):
            if self.connections[i].a == self.locations[a_idx] and self.connections[i].b == self.locations[b_idx]:
                con = self.connections[i]
            if self.connections[i].b == self.locations[a_idx] and self.connections[i].a == self.locations[b_idx]:
                con = self.connections[i]
        return con

    def __distance(self, current_idx, end_idx):
        return Connection(self.locations[current_idx], self.locations[end_idx]).distance()

    def __get_location_index(self, a: Location):
        for i in range(len(self.locations)):
            if a == self.locations[i]:
                return i
        raise Exception('no such location')

    def __get_lowest_score_node(self, open, scores):
        lowest = 2147800000  # Infinity
        key = 0
        for i in range(len(open)):
            if scores[open[i]] < lowest:
                lowest = scores[open[i]]
                key = open[i]
        return key

    def __get_loc_neighbours(self, loc: Location):
        neighbours = []
        for i in range(len(self.connections)):
            if self.connections[i].a == loc:
                neighbours.append(
                    self.__get_location_index(self.connections[i].b))
            if self.connections[i].b == loc:
                neighbours.append(
                    self.__get_location_index(self.connections[i].a))
        return neighbours
