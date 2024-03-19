import random
from plexi import Bitmap
from plexi.coords import neighbors
from plexi.color import RED, mix

bmp = Bitmap.load(r"C:\Users\frs\source\repos\privat\plexi-test\pikachu2.bmp")

def is_same_color(color1, color2, tolerance=64):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return abs(r1-r2) + abs(g1-g2) + abs(b1-b2) <= tolerance


def get_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    dx, dy = x2-x1, y2-y1
    return dx*dx + dy*dy

def get_closest(coord, sample):
    min_distance = None
    closest_coord = None
    for sample_coord in sample:
        distance = get_distance(coord, sample_coord)
        if not closest_coord or distance < min_distance:
            min_distance = distance
            closest_coord = sample_coord
    return closest_coord

def voronoi(bmp, sample_size=1000):
    sample = random.sample(list(bmp.keys()), sample_size)

    for coord in bmp:
        bmp[coord] = bmp[get_closest(coord, sample)]

def fuzz(bmp):
    for coord in bmp:
        fuzzed = {}
        colors_to_mix = list()
        for nbor in neighbors(coord, including_me=True):
            if nbor not in bmp:
                continue
            else:
                colors_to_mix.append(bmp[nbor])
        mixed_color = mix(colors_to_mix)
        fuzzed[coord] = mixed_color
    bmp.set_many(fuzzed.items())

def is_whitish(color):
    r, g, b = color
    return r > 100 and g > 100 and b > 100

def get_group_from(bmp, coord):
    base_color = bmp[coord]
    edge = [coord]
    group = set()
    while edge:
        c = edge.pop()
        for nbor in neighbors(c):
            if nbor in bmp and nbor not in group and is_same_color(bmp[nbor], base_color):
                edge.append(nbor)
                group.add(nbor)
    return group

def invert(color):
    r, g, b = color
    return 255-r, 255-g, 255-b

bg = get_group_from(bmp, (0,0))

for coord in bmp:
    if coord in bg:
        continue
    bmp[coord] = invert(bmp[coord])

bmp.save("out.bmp")
