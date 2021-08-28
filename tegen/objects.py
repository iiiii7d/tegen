import blessed

import tegen.pixel as pixel

class Object:
    """The base class of all objects.
    
    .. versionadded:: 0.0"""

    def __init__(self):
        self.x: int = None
        self.y: int = None

    def edges(self):
        pass

    def on_init(self, g):
        """This method is to be overridden when extended.
        Called on scene load.

        .. versionadded:: 0.0

        :param Game g: The game object"""
        pass

    def on_end(self, g):
        """This method is to be overridden when extended.
        Called on scene unload.

        .. versionadded:: 0.0

        :param Game g: The game object"""
        pass

    def pre_update(self, g):
        """This method is to be overridden when extended.
        Called every tick of the game loop, before :py:meth:`update`.

        .. versionadded:: 0.0

        :param Game g: The game object"""
        pass

    def update(self, g):
        """This method is to be overridden when extended.
        Called every tick of the game loop.

        .. versionadded:: 0.0

        :param Game g: The game object"""
        pass

    def post_update(self, g):
        """This method is to be overridden when extended.
        Called every tick of the game loop, after :py:meth:`update`.

        .. versionadded:: 0.0

        :param Game g: The game object"""
        pass

    def on_keyboard_press(self, g, key: str):
        """This method is to be overridden when extended.
        Called on a key press.

        .. versionadded:: 0.0

        :param Game g: The game object
        :param str key: The key pressed"""


class Screen(Object):
    """Inherited from :py:class:`Object`. Represents the screen.
    
    .. versionadded:: 0.0
    
    :param int x: The game x coordinate of the topleft corner
    :param int y: The game y coordinate of the topleft corner"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def corners(self):
        """Returns the global coordinates of the four corners of the screen.
        
        .. versionadded:: 0.0
        
        :returns: A list of coordinates, in the form ``[tl, tr, bl, br]``
        :rtype: List[Tuple[int, int]]"""
        term = blessed.Terminal()
        tl = self.x, self.y
        tr = self.x+term.width-1, self.y
        bl = self.x, self.y+term.height-1
        br = self.x+term.width-1, self.y+term.height-1
        return [tl, tr, bl, br]

    def edges(self):
        """Returns the global x coordinate of the leftmost and rightmost columns,
        and the global y coordinate of the topmost and bottommost rows of the screen.

        .. versionadded:: 0.0

        :returns: A tuple of values, in the form ``[lx, rx, ty, by]``
        :rtype: Tuple[int, int, int, int]"""
        term = blessed.Terminal()
        lx = self.x
        rx = self.x+term.width-1
        ty = self.y
        by = self.y+term.height-1
        return lx, rx, ty, by


class Sprite(Object):
    """Inherited from :py:class:`Object`. Represents a sprite.

    .. versionadded:: 0.0"""
    pixels = pixel.from_2d_array(fore=[['f00', 'aaa', 'f00'],
                                       ['aaa', 'f00', 'aaa'],
                                       ['f00', 'aaa', 'f00']],
                                 char=['███',
                                       '███',
                                       '███'])

    def edges(self):
        """Returns the global x coordinate of the leftmost and rightmost columns,
        and the global y coordinate of the topmost and bottommost rows of the screen.

        .. versionadded:: 0.0

        :returns: A tuple of values, in the form ``[lx, rx, ty, by]``
        :rtype: Tuple[int, int, int, int]"""
        lx, ty = (float("inf"),)*2
        rx, by = (0,)*2
        for local_x, local_y in list(self.pixels.keys()):
            if local_x > rx: rx = local_x
            if local_x < lx: lx = local_x
            if local_y > by: by = local_y
            if local_y < ty: ty = local_y
        
        return self.x+lx, self.x+rx, self.y+ty, self.y+by

    def local_move(self, x: int, y: int):
        """Move the sprite's local coordinates.

        .. versionadded:: 0.0

        :param x: The local x value to move the coordinates by
        :param y: The local y value to move the coordinates by
        """
        new_pixels = {}
        for coords, pixel_dict in self.pixels.items():
            new_coords = (coords[0]+x, coords[1]+y)
            new_pixels[new_coords] = pixel_dict
