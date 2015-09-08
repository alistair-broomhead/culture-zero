from coords import Coordinate


class Hex(object):
    def __init__(self, map_, coord):
        assert isinstance(coord, Coordinate)

        self.map = map_
        self.coord = coord

        self.terrain = None
        self.utility = None
        self.improvement = None
        self.units = []

    @staticmethod
    def _draw_part(part, screen_coord):
        if part is not None:
            part.centerx = screen_coord.x
            part.centery = screen_coord.y
            part.draw()

    def draw(self, camera):
        screen_coord = camera.get_screen_coord(self.coord)

        if screen_coord is None:
            return

        self._draw_part(self.terrain, screen_coord)
        self._draw_part(self.utility, screen_coord)
        self._draw_part(self.improvement, screen_coord)
        for unit in self.units:
            self._draw_part(unit, screen_coord)


class Map(object):
    """
    Map of hex tiles on even-q coordinate system
    """
    def __init__(self, radius):
        self.grid = {}

        for x in range(-radius, radius+1):
            z_min = max((-radius, -radius - x))
            z_max = min((radius, radius - x))
            for z in range(z_min, z_max+1):
                coord = Coordinate()
                coord.axial = x, z

                self.grid[coord] = Hex(self, coord)

    def draw(self, camera):
        drawn = 0
        for tile in sorted(self.grid.values(),
                           key=lambda t: (t.coord.cube.z, t.coord.cube.x)):
            if camera.get_screen_coord(tile.coord):
                tile.draw(camera)
                drawn += 1
