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

class Sprite(Object):
    """Inherited from :py:class:`Object`. Represents a sprite.

    .. versionadded:: 0.0"""
    pixels = pixel.from_2d_array([['00ff00', '00ff00'],
                                  ['00ff00', '00ff00']])