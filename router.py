import random


def distance_between(a, b):
    """
    Computes the euclidian distance between two locations.
    """
    return ((((b.x - a.x)**2) + ((b.y-a.y)**2))**0.5)


def closest_not_connected_neighbour(loc, connections, locations):
    """
    This function attempts to find the closest location to `loc` which is not directory connected to it.
    """

    closest_neighbour_distance = 1_000_000_000  # We set this to almost infinity
    closest_neighbour = None

    for other_loc in locations:
        # We don't want to connect a location with itself.
        if loc == other_loc:
            continue

        # We make sure that we haven't already connected these two locations.
        already_connected = False
        for connection in connections:
            if (connection[0] == loc and connection[1] == other_loc) or (connection[0] == other_loc and connection[1] == loc):
                already_connected = True
        if already_connected:
            continue

        # We compute the distance and see if it's closer than our best current guess.
        distance = distance_between(loc, other_loc)
        if distance < closest_neighbour_distance:
            closest_neighbour = other_loc
            closest_neighbour_distance = distance

    return closest_neighbour


def connect_locations(locations, connect):
    """
    You are given a list of locations that you must connect together using the `connect` function.
    Calling connect multiple times with the same locations is idempotent.
    """

    # We declare a list to store which locations we already connected.
    connections = []

    # For each location in the map.
    for loc in locations:

        # Find its closest neightbour with which it's not connected.
        neighbour = closest_not_connected_neighbour(
            loc, connections, locations)

        # If we found no suitable neighbour we skip this location.
        if neighbour == None:
            continue

        # Connect them
        connect(loc, neighbour)

        # Store this new connection in our connections list
        connections.append((loc, neighbour))
