from collections import namedtuple

CubeCoord = namedtuple("CubeCoord", "x,y,z")
AxialCoord = namedtuple("AxialCoord", "q,r")
SQRT_3 = 3.0 ** 0.5


class PixelCoord(object):
    """
    Like a namedtuple("PixelCoord", "x,y") but with a scale that defaults to 1.0
    """
    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self._scale = scale

    def copy(self):
        return PixelCoord(self.x, self.y, self._scale)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        value = float(value)

        factor = value / self._scale
        self._scale = value
        self.x *= factor
        self.y *= factor

    def scaled(self, scale):
        coord = self.copy()
        coord.scale = scale
        return coord

    def __iter__(self):
        yield self.x
        yield self.y

    def __sub__(self, other):
        assert other.scale == self._scale

        return PixelCoord(self.x - other.x,
                          self.y - other.y,
                          self._scale)

    def __add__(self, other):
        assert other.scale == self._scale

        return PixelCoord(self.x + other.x,
                          self.y + other.y,
                          self._scale)

    def __eq__(self, other):
        return all((
            self.x == other.x,
            self.y == other.y,
            self._scale == other.scale
        ))


class Coordinate(object):
    CubeCoord = CubeCoord
    AxialCoord = AxialCoord
    PixelCoord = PixelCoord

    _x = _y = _z = 0

    @property
    def cube(self):
        return CubeCoord(self._x, self._y, self._z)

    @staticmethod
    def _round_cube(value):
        cube_x, cube_y, cube_z = value

        r_x = round(cube_x)
        r_y = round(cube_y)
        r_z = round(cube_z)

        diff_x = abs(r_x - cube_x)
        diff_y = abs(r_y - cube_y)
        diff_z = abs(r_z - cube_z)

        if diff_x > diff_y and diff_x > diff_z:
            r_x = 0 - r_y - r_z
        elif diff_y > diff_z:
            r_y = 0 - r_x - r_z
        else:
            r_z = 0 - r_x - r_y

        return r_x, r_y, r_z

    @cube.setter
    def cube(self, value):
        if not all(isinstance(cube_coord, int) for cube_coord in value):
            value = self._round_cube(value)

        self._x, self._y, self._z = value

    @property
    def axial(self):
        return AxialCoord(self._x, self._z)

    @axial.setter
    def axial(self, value):
        axial_q, axial_r = value

        x = axial_q
        y = 0 - axial_q - axial_r
        z = axial_r

        self.cube = x, y, z

    @property
    def world(self):
        q, r = self.axial
        q_by_2 = q * 0.5

        world_x = q_by_2 * 3
        world_y = (r + q_by_2) * SQRT_3

        return PixelCoord(world_x, world_y)

    @world.setter
    def world(self, value):

        assert isinstance(value, PixelCoord)
        assert value.scale == 1.0

        x, y = value

        q = x * 2.0 / 3.0
        r = (0 - x / 3.0) + (y * SQRT_3 / 3.0)

        self.axial = q, r
