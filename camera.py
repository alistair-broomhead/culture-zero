from coords import PixelCoord


class Camera(object):
    def __init__(self, x_size, y_size):

        self.pos = PixelCoord(0, 10, scale=30)

        self._screen_size = None
        self._screen_centre_x = None
        self._screen_centre_y = None

        self.screen_size = x_size, y_size

        self._calc_pos = None
        self._screen_bounds = None

    @property
    def screen_size(self):
        return self._screen_size

    @screen_size.setter
    def screen_size(self, value):
        x_size, y_size = value
        self._screen_size = x_size, y_size
        self._screen_centre_x = x_size / 2
        self._screen_centre_y = y_size / 2

    @property
    def screen_bounds(self):
        if self._screen_bounds is None or self._calc_pos != self.pos:

            print("CALCULATE BOUNDS:", end='')

            self._calc_pos = self.pos.copy()

            screen_width, screen_height = self.screen_size

            tile_width = self.pos.scale * 2.0
            tile_height = self.pos.scale * 2.0

            half_draw_width = (screen_width + tile_width) / 2
            half_draw_height = (screen_height + tile_height) / 2

            min_x = - half_draw_width
            max_x = + half_draw_width
            min_y = - half_draw_height
            max_y = + half_draw_height

            self._screen_bounds = min_x, max_x, min_y, max_y

            print(self._screen_bounds)

        return self._screen_bounds

    def get_screen_coord(self, coordinate):
        p_coord = coordinate.world.scaled(self.pos.scale)

        min_x, max_x, min_y, max_y = self.screen_bounds

        offset_coord = p_coord - self.pos

        if min_x <= offset_coord.x <= max_x:
            if min_y <= offset_coord.y <= max_y:
                return offset_coord + PixelCoord(self._screen_centre_x,
                                                 self._screen_centre_y,
                                                 p_coord.scale)

        return None
