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

    def on_end(self, g):
        """This method is to be overridden when extended.
        Called on scene unload.

        .. versionadded:: 0.0

        :param Game g: The game object"""

    def pre_update(self, g):
        """This method is to be overridden when extended.
        Called every tick of the game loop, before :py:meth:`update`.

        .. versionadded:: 0.0

        :param Game g: The game object"""

    def update(self, g):
        """This method is to be overridden when extended.
        Called every tick of the game loop.

        .. versionadded:: 0.0

        :param Game g: The game object"""

    def post_update(self, g):
        """This method is to be overridden when extended.
        Called every tick of the game loop, after :py:meth:`update`.

        .. versionadded:: 0.0

        :param Game g: The game object"""

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
    """Inherited from :py:class:`Object`. Represents some text on a screen.

    .. versionadded:: 0.0

    :param str text: The text to start with
    :param back: The background colour of the text
    :type back: Tuple[int, int, int]
    :param fore: The foreground colour of the text
    :type fore: Tuple[int, int, int]
    
    .. py:attribute:: anchor
       :type: str
    
       The anchor of text, one of ``tr``, ``tl``, ``br``, ``bl``, ``center``

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
        text = self.text
        w = max([len(l) for l in text.split("\n")])
        h = text.count('\n')
        if self.anchor == "center":
            ox = round(w / 2)
            oy = round(h / 2)
        else:
            if self.anchor not in ['tr', 'tl', 'br', 'bl']:
                raise ValueError("'anchor' is not one of 'center', 'tr', 'tl', 'br', 'bl'")
            ox = 0 if self.anchor[1] == 'l' else w - 0
            oy = 0 if self.anchor[0] == 't' else h - 0
        result = {}
        for line_num, line in enumerate(text.split('\n')):
            for char_num, char in enumerate(line):
                result[char_num-ox, line_num-oy] = char
        return result

class TextInput(Text):
    """Inherited from :py:class:`Text`. Represents a text input box.
    
    .. versionadded:: 0.1

    .. warning:: Triggering this would take the ID `/{TextInput.id}.cursor/` as well for the cursor
    
    .. py:attribute:: game
       :type: Game
       
       The game that the text input is attached to. Is ``None`` when not triggered.
       
       .. versionadded:: 0.1

    .. py:attribute:: cursor
       :type: TextInput.Cursor
       
       The cursor of the text input. Is ``None`` when not triggered.
       
       .. versionadded:: 0.1"""
    
    class Cursor(Sprite):
        """Inherited from :py:class:`Sprite`. Represents the cursor of :py:class:`TextInput`.
        
        .. versionadded:: 0.1
        
        .. py:attribute:: text_pos
           :type: int
       
           The position of the cursor in the text, or the position of the character that has yet to be entered in.
           
            .. versionadded:: 0.1

           .. py:attribute:: text_pos
           :type: int
       
           The line that the cursor is at
           
           .. versionadded:: 0.1"""
        text_pos = 0
        line = 0

    game = None
    cursor: Cursor = None
    def trigger(self, game):
        """Triggers the text input and enters input mode.

        .. versionadded:: 0.1

        :param Game game: The game object"""
        if game.current_text_input is not None: game.current_text_input.release()
        game.current_text_input = self
        self.game = game
        self.cursor = self.Cursor()
        self.cursor.text_pos = len(self.text)
        self.cursor.pixels = pixel.from_2d_array(char=[" "],
                                                 back=[[0x808080 if self.back is None else 0xffffff-self.back]])
        x = self.x + len(self.text.split("\n")[-1])
        y = self.y + self.text.count("\n")
        game.add_object(self.cursor, f"/{self.id}.cursor/", x, y, override=True)
        game.wait_until_key_released()

    def on_keyboard_press(self, game, key: Keystroke):
        """:meta private:"""
        if self.game is None: return
        if key.is_sequence:
            if key.name == 'KEY_ENTER':
                self.text = self.text[:self.cursor.text_pos] + "\n" + self.text[self.cursor.text_pos:]
                self.cursor.y += 1
                self.cursor.line += 1
                self.cursor.x = self.x
                self.cursor.text_pos += 1
            elif key.name == 'KEY_ESCAPE':
                self.release()
            elif key.name == 'KEY_BACKSPACE':
                if self.text == "" or self.cursor.text_pos == 0: return
                char = self.text[self.cursor.text_pos-1]
                self.text = self.text[:self.cursor.text_pos-1] + self.text[self.cursor.text_pos:]
                if char != "\n":
                    self.cursor.x -= 1
                else:
                    self.cursor.y -= 1
                    self.cursor.line -= 1
                    self.cursor.x = self.x + len(self.text.split("\n")[self.cursor.line])
                self.cursor.text_pos -= 1
            elif key.name == 'KEY_DELETE':
                if self.text == "" or self.cursor.text_pos == len(self.text): return
                char = self.text[self.cursor.text_pos]
                self.text = self.text[:self.cursor.text_pos] + self.text[self.cursor.text_pos+1:]
            elif key.name == 'KEY_RIGHT':
                if self.cursor.text_pos == len(self.text): return
                if self.text[self.cursor.text_pos] == "\n":
                    self.cursor.line += 1
                    self.cursor.x = self.x
                    self.cursor.y += 1
                else:
                    self.cursor.x += 1
                self.cursor.text_pos += 1
            elif key.name == 'KEY_LEFT':
                if self.cursor.text_pos == 0: return
                if self.text[self.cursor.text_pos-1] == "\n":
                    self.cursor.line -= 1
                    self.cursor.x = len(self.text.split("\n")[self.cursor.line])
                    self.cursor.y -= 1
                else:
                    self.cursor.x -= 1
                self.cursor.text_pos -= 1
        else:
            self.text = self.text[:self.cursor.text_pos] + str(key) + self.text[self.cursor.text_pos:]
            self.cursor.x += 1
            self.cursor.text_pos += 1

    def release(self):
        """Releases the text input and exits input mode.

        .. versionadded:: 0.1"""
        self.game.remove_object_by_id(f"/{self.id}.cursor/", nonexist_error=False)
        self.game.current_text_input = None
        self.game = None
