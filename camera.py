from coords import PixelCoord


class Camera(object):
    _screen_size = None
    _screen_centre_x = None
    _screen_centre_y = None

    _calc_pos = None
    _screen_bounds = None

    def __init__(self, x_size, y_size, scale=30):
        self.pos = PixelCoord(0, 0, scale)
        self.screen_size = x_size, y_size

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

            self._calc_pos = self.pos.copy()

            screen_width, screen_height = self.screen_size

            half_draw_width = (screen_width / 2) + self.pos.scale
            half_draw_height = (screen_height / 2) + self.pos.scale

            self._screen_bounds = (
                0 - half_draw_width,
                0 + half_draw_width,
                0 - half_draw_height,
                0 + half_draw_height,
            )

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
