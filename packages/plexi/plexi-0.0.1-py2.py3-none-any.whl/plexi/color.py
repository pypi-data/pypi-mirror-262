from collections import namedtuple


Color = namedtuple("Color", ["r", "g", "b"])

BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)


def mix(colors : list[Color]):
    color_list = list(colors)
    rs, gs, bs = zip(*color_list)
    length = len(color_list)
    return Color(sum(rs)//length, sum(gs)//length, sum(bs)//length)
