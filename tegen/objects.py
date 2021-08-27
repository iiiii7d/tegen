import blessed
import tegen.pixel as pixel

class Object:
    """The base class of all objects.
    
    .. versionadded:: 0.0"""

    def on_init(self, game):
        """This method is to be overridden when extended.
        Called on scene load."""
        pass

    def on_end(self, game):
        """This method is to be overridden when extended.
        Called on scene unload."""
        pass

    def pre_update(self, game):
        """This method is to be overridden when extended.
        Called every tick of the game loop, before :py:meth:`update`."""
        pass

    def update(self, game):
        """This method is to be overridden when extended.
        Called every tick of the game loop."""
        pass

    def post_update(self, game):
        """This method is to be overridden when extended.
        Called every tick of the game loop, after :py:meth:`update`."""
        pass

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
    pixels = pixel.from_2d_array(fore=[['00ff00', '00ff00'],
                                       ['00ff00', '00ff00']],
                                 char=['██',
                                       '██'])

    def edges(self, x: int=0, y: int=0):
        """Returns the global x coordinate of the leftmost and rightmost columns,
        and the global y coordinate of the topmost and bottommost rows of the screen.

        .. versionadded:: 0.0

        :param int x: The global x coordinate of the anchor
        :param int y: The global y coordinate of the anchor
        :returns: A tuple of values, in the form ``[lx, rx, ty, by]``
        :rtype: Tuple[int, int, int, int]"""
        lx, ty = (float("inf"),)*2
        rx, by = (0,)*2
        for local_x, local_y in list(self.pixels.keys()):
            if local_x > rx: rx = local_x
            if local_x < lx: lx = local_x
            if local_y > by: by = local_y
            if local_y < ty: ty = local_y
        
        return x+lx, x+rx, y+ty, y+by