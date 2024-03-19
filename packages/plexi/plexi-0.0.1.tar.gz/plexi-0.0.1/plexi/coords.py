from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])

def up(coord):
    x, y = coord
    return coord.__class__(x, y+1)

def right(coord):
    x, y = coord
    return coord.__class__(x+1, y)

def down(coord):
    x, y = coord
    return coord.__class__(x, y-1)

def left(coord):
    x, y = coord
    return coord.__class__(x-1, y)

def neighbors(coord, including_me=False):
    "Yields the coordinates of the neighbors of (x, y)"
    x, y = coord
    if including_me:
        yield coord
    yield x, y+1
    yield x+1, y
    yield x, y-1
    yield x-1, y
