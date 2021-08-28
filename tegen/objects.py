from typing import List, Tuple, Dict, Optional
import blessed
from blessed.keyboard import Keystroke

import tegen.pixel as pixel


class Object:
    """The base class of all objects.
    
    .. versionadded:: 0.0
    
    .. py:attribute:: x
       :type: int
    
       The global x coordinate of the object, set when added to a scene
       
       .. versionadded:: 0.0
       
    .. py:attribute:: y
       :type: int
    
       The global y coordinate of the object, set when added to a scene
       
       .. versionadded:: 0.0
       
    .. py:attribute:: id
       :type: str
    
       The ID of the object, set when added to a scene
       
       .. versionadded:: 0.0"""

    def __init__(self):
        self.x: int = None
        self.y: int = None
        self.id: str = None

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

    def on_keyboard_press(self, g, key: Keystroke):
        """This method is to be overridden when extended.
        Called on a key press.

        .. versionadded:: 0.0

        :param Game g: The game object
        :param Keystroke key: The key pressed"""


class Screen(Object):
    """Inherited from :py:class:`Object`. Represents the screen.
    
    .. versionadded:: 0.0
    
    :param int x: The game x coordinate of the topleft corner
    :param int y: The game y coordinate of the topleft corner"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def corners(self) -> List[Tuple[int, int]]:
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

    def edges(self) -> Tuple[int, int, int, int]:
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

    def edges(self) -> Tuple[int, int, int, int]:
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

class Text(Object):
    """Represents some text on a screen.

    .. versionadded:: 0.0

    :param str text: The text to start with
    :param back: The background colour of the text
    :type back: Tuple[int, int, int]
    :param fore: The foreground colour of the text
    :type fore: Tuple[int, int, int]
    
    .. py:attribute:: anchor
       :type: str
    
       The anchor of text

       .. versionadded:: 0.0
       
    .. py:attribute:: text
       :type: str
       
       The content of the text

       .. versionadded:: 0.0

    .. py:attribute:: back
       :type: Tuple[int, int, int]

       The background colour of the text

       .. versionadded:: 0.0

    .. py:attribute:: fore
       :type: Tuple[int, int, int]

       The foreground colour of the text

       .. versionadded:: 0.0"""

    anchor = 'tl'
    back: Tuple[int, int, int] = None
    fore: Tuple[int, int, int] = None

    def __init__(self, text: str, back: Optional[pixel.Colour]=None, fore: Optional[pixel.Colour]=None):
        super().__init__()
        self.text = text
        if back is not None: self.back = pixel._parse_colours(back) # noqa
        if fore is not None: self.fore = pixel._parse_colours(fore) # noqa

    def edges(self) -> Tuple[int, int, int, int]:
        """Returns the global x coordinate of the leftmost and rightmost columns,
        and the global y coordinate of the topmost and bottommost rows of the screen.

        .. versionadded:: 0.0

        :returns: A tuple of values, in the form ``[lx, rx, ty, by]``
        :rtype: Tuple[int, int, int, int]"""
        w = max([len(l) for l in self.text.split("\n")])
        h = self.text.count('\n')+1
        return self.x, self.x+w-1, self.y, self.y+h-1

    def get_char_positions(self) -> Dict[tuple, str]:
        """Get the positions of each character relative to the anchor.

        .. versionadded:: 0.0

        :returns: A dict in the form ``{(local x, local y): char}``
        :rtype: Dict[tuple, str]
        :raises ValueError: if ``anchor`` is not one of ``tr``, ``tl``, ``br``, ``bl``, ``center``"""
        w = max([len(l) for l in self.text.split("\n")])
        h = self.text.count('\n')
        if self.anchor == "center":
            ox = round(w / 2)
            oy = round(h / 2)
        else:
            if self.anchor not in ['tr', 'tl', 'br', 'bl']:
                raise ValueError("'anchor' is not one of 'center', 'tr', 'tl', 'br', 'bl'")
            ox = 0 if self.anchor[1] == 'l' else w - 0
            oy = 0 if self.anchor[0] == 't' else h - 0
        result = {}
        for line_num, line in enumerate(self.text.split('\n')):
            for char_num, char in enumerate(line):
                result[char_num-ox, line_num-oy] = char
        return result

