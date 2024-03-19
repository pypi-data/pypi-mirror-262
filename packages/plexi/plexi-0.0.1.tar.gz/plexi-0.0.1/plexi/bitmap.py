from importlib.resources import files
import io

import itertools
from .io_ import save_to_stream, load_from_stream
from .coords import Coordinate
from .color import Color

class Bitmap:
    def __init__(self, width : int, height : int, color=(0, 0, 0)):
        """
        width: The width of the bitmap, in pixels
        height: The height of the bitmap, in pixels
        color: The color of the bitmap, as an RGB tuple
        """
        self.width = width
        self.height = height
        self._lines = list()
        for _ in range(self.height):
            line = []
            for _ in range(self.width):
                line.append(color)
            self._lines.append(line)

    def __getitem__(self, coord : Coordinate):
        x, y = coord
        if coord in self:
            return self._lines[y][x]
        else:
            raise KeyError(coord)

    def __setitem__(self, coord : Coordinate, color : Color):
        x, y = coord
        if coord in self:
            self._lines[y][x] = color
        else:
            raise KeyError(coord)

    def __iter__(self):
        for x, y in itertools.product(range(self.width), range(self.height)):
            yield Coordinate(x, y)

    def __contains__(self, coord : Coordinate):
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, coord : Coordinate):
        if coord in self:
            return self[coord]
        else:
            return None
        
    def set_many(self, items):
        for coord, color in items:
            self[coord] = color

    def keys(self):
        return iter(self)

    def items(self):
        for key in self:
            yield key, self[key]

    def values(self):
        for key in self:
            yield self[key]

    def save(self, path):
        with open(path, 'wb') as s:
            return save_to_stream(self, s)

    @classmethod
    def from_dict(cls, d : dict):
        xs, ys = zip(*d.keys())
        bmp = cls(max(xs)+1, max(ys)+1)
        for coord, color in d.items():
            bmp[coord] = color
        return bmp


    @classmethod
    def load(cls, path):
        with open(path, 'rb') as s:
            return load_from_stream(cls, s)

    @classmethod
    def get_sample(cls, name):
        bmp_bytes = files('plexi').joinpath('images', f'{name}.bmp').read_bytes()
        bmp_stream = io.BytesIO(bmp_bytes)
        return load_from_stream(Bitmap, bmp_stream)

