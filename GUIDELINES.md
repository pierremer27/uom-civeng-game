# Railway Planner Guidelines

This document describes how to play the game.

## Introduction

Railway Planner is a game that lets you, the player, come up with an algorithm to connect a bunch of locations together to create an efficient railway system. Think of it as if you were responsible for designing your city's metro or train system.

When implementing your algorithm, you must think of the real-world constraints you face when building a transportation system:
- How much money does my railway network cost?
- How fast is it? Do people get to their destination on time?
- Is tarffic distributed equally in your network? Is there congestion on some axis?

The game implements these constraints and forces you to come up with an efficient algorithm:
- If you build lots and lots of railways (aka too many connections), your network will cost too much money.
- If you don't connect locations efficiently, people will spend too much time getting from point A to point B.
- If some parts of your network are used too often and some almost never, you will get a bad congestion rating.

## Implementing your algorithm

Before implementing an algorithm, you should test that the game works when you run the following command:

```
python3 run.py levels/manchester.json
```

A window should pop up and animations should start playing. At the end, you should be able to see the **total cost** of the network, the **average travel time** (the average time it takes for a passenger to go from point A to point B) and the **traffic congestion rating** (higher values mean poor traffic distribution).

Okay let's implement your algorithm! Open the file `router.py` with a text editor suitable for programming.

Inside this file there is a `connect_locations` function. It is this function you must implement to construct your network. Let's look at how to connect two locations.

Okay so, inside our `connect_locations` we have access to two variables:
- `locations`: a list of location objects.
- `connect`: a function which you can call to connect two locations.

```python
def connect_locations(locations, connect):
    # Here we print the first location in the list.
    print(locations[0])
    # Here we print the coordinates of our location.
    print(locations[0].x, locations[0].y)
    # Here we connect the first location in the list with the second.
    connect(locations[0], locations[1])
```

You can try to run this code already! This simple algorithm simply connects two locations. When launching the game you should see two locations connected by a gray line.

Your network has also been evaluated by the system. You should be able to see the cost of this single connection, the time it takes to connect the two points and finally the traffic congestion rating (should be zero as traffic is perfectly distributed as there is only one connection).

You should also see a popup warning you that your network is incompltete. You should make sure that every location is accessible!

Let's tweak our algorithm a bit. Let's try to connect every single location at once.

```python
def connect_locations(locations, connect):
    # Code to connect every point with each other.
    # This solution is not optimal at all because it uses too much resources.
    for loc_1 in locations:
        for loc_2 in locations:
            connect(loc_1, loc_2)
```

When running the game with this code, you should see that every location has a **direct connection** to each and every one of its neighbors.

If we look at our score, we should see that the cost of our network is **extremely high**. In fact, creating a connection is expensive and this network is not feasible.

However we notice that the **average travel time** is low. In fact, it is optimal because for each commute route, we take the shortest possible path. Our congestion is almost zero, because the load is distributed evenly (each connection is used exactly once).

Let's try one last approach. Let's build a network that's completely random!

```python
import random

def connect_locations(locations, connect):
    for loc_1 in locations:
        for loc_2 in locations:
            if random.randint(0, 4) == 0:
                connect(loc_1, loc_2)
```

Now every time you launch your game, you should see a new network with a different score everytime.

Now your turn! Try to implement your own algorithm and try aiming for the lowest cost possible while still maintaining low congestion and travel time.

If you manage to create a good enough algorithm, try to test it on another city to see how well it adapts!

```
python3 run.py levels/paris.json
```
