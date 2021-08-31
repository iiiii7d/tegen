from typing import Union, Tuple, Optional, Dict, List
import blessed
import threading
import time
import math
import traceback

from tegen.scene import Scene
from tegen.objects import Screen, Sprite, Object, Text, TextInput
import tegen.pixel as pixel

class Game:
    """The entry point for the game.
    
    .. versionadded:: 0.0
    
    .. py:attribute:: game_on
       :type: bool
       
       Whether the game is running.
       
       .. versionadded:: 0.0
       
    .. py:attribute:: loop
       :type: threading.Thread
       
       The looping thread of the game.
       
       .. versionadded:: 0.0

    .. py:attribute:: keyboard_listener
       :type: threading.Thread

       The keyboard listening thread of the game.

       .. versionadded:: 0.0
       
    .. py:attribute:: objects
       :type: Dict[object, dict]
       
       A list of objects currently loaded.
       
       .. versionadded:: 0.0

    .. py:attribute:: screen
       :type: Screen

       The screen object of the game.

       .. versionadded:: 0.0

    .. py:attribute:: current_scene
       :type: Scene

       The current scene that the game is showing.

       .. versionadded:: 0.0

    .. py:attribute:: speeds
       :type: List[float]

       A list of milliseconds per frame.

       .. versionadded:: 0.0
       
    .. py:attribute:: current_text_input
       :type: TextInput
       
       The text input that is currently triggered. Is ``None`` if there is no inputs triggered.
       
       .. versionadded:: 0.1"""
    
    term = blessed.Terminal()

    def __init__(self):
        self.game_on = False
        self.loop: threading.Thread = None
        self.keyboard_listener: threading.Thread = None
        self.objects: Dict[tuple, Object] = {}
        self.screen = Screen(0, 0)
        self.current_scene: Scene = None
        self.speeds: List[float] = []
        self.current_text_input: TextInput = None

    def start(self, show_info: bool=True, info_wait: Union[int, float]=3):
        """Starts the game.

        .. versionadded:: 0.0

        :param bool show_info: Whether to show tegen and terminal info before the game starts
        :param info_wait: The amount of time for tegen and terminal info to show
        :type info_wait: int or float"""
        term = self.term
        print(term.height*"\n")
        print(term.home + term.clear, end='')
        if show_info:
            from tegen import __version__
            print(term.bold("tegen v"+__version__))
            print("number of colours: "+str(term.number_of_colors))
            print("terminal size (h,w): "+str((term.height, term.width)))
            time.sleep(info_wait)
        print(term.home + term.clear, end='')
        self.game_on = True
        self.loop = threading.Thread(target=_loop, args=(self,))
        self.loop.start()
        
    def end(self):
        """Ends the game.

        .. versionadded:: 0.0"""
        term = self.term
        for id_, obj in self.objects.items():
            obj.on_end(self)
        self.game_on = False
        print(term.home + term.clear + term.bright_yellow("Stopping..."), end='')
        time.sleep(0.5)
        print(term.home + term.clear, end='')

    def load_scene(self, scene: Scene, clear_objects: bool=True):
        """Loads a scene to the game.

        .. versionadded:: 0.0

        :param Scene scene: The scene to load
        :param bool clear_objects: Whether to clear all objects in the previous scene before loading the new scene"""
        for id_, obj in self.objects.items():
            obj.on_end(self)
        self.current_scene = scene
        if clear_objects: self.objects.clear()
        self.objects.update(scene.objects)
        for id_, obj in self.objects.items():
            obj.on_init(self)

    def save_scene(self) -> Scene:
        """Saves the current game as a scene.
        
        .. versionadded:: 0.1
        
        :rtype: Scene"""
        scene = Scene()
        for k, v in self.objects.items():
            scene.add_object(v, k, v.x, v.y)
        return scene

    def call_event(self, event: str, *args, **kwargs):
        """Calls an event, running `on_<event name>` in all :py:class:`Object` s, if present.
        
        .. versionadded:: 0.0
        
        :param str event: The name of the event to call"""
        def empty():
            pass

        items = list(self.objects.items())[:]
        for id_, obj in items:
            getattr(obj, 'on_'+event, empty)(self, *args, **kwargs) # noqa

    def add_object(self, obj: Object, id_: str, x: float, y: float, override: bool = False):
        """Adds an :py:class:`Object` to the game.

        .. versionadded:: 0.0

        :param Object obj: The object to add
        :param str id_: The ID to give to the object
        :param float x: The global x coordinate of the anchor (local x=0)
        :param float y: The global y coordinate of the anchor (local y=0)
        :param bool override: Whether to override the existing object, if an object with the same ID exists
        :raises ValueError: if the ``obj`` is a :py:class:`Screen`
        :raises KeyError: if an object with the same ID exists and ``override`` is False"""
        if isinstance(obj, Screen):
            raise ValueError("Object added cannot be a screen, access the screen via `Game.screen`")
        if id_ in self.objects.keys() and not override:
            raise KeyError(f"Object '{id_}' already exists")
        obj.id = id_
        obj.x = x
        obj.y = y
        self.objects[id_] = obj
        obj.on_init(self)

    def remove_object_by_id(self, id_: str, nonexist_error: bool = False):
        """Removes an :py:class:`Object` from the game by its ID.

        .. versionadded:: 0.0

        :param str id_: The ID of the object to remove
        :param bool nonexist_error: Whether to raise an error if an object does not exist in the game."""
        try:
            self.objects[id_].on_end(self)
            del self.objects[id_]
        except KeyError as e:
            if nonexist_error: raise e

    def remove_object_by_class(self, cls: type) -> int:
        """Removes :py:class:`Object` s from the game by their class type.

        .. versionadded:: 0.0

        .. versionchanged:: 0.1
           Now returns the number of objects removed

        :param type cls: The class, should be a subclass of :py:class:`Object`
        :raises TypeError: if the class is not a subclass of :py:class:`Object`
        :returns: The number of objects removed
        :rtype: int"""
        if not issubclass(cls, Object):
            raise TypeError("Class is not subclass of Object")
        count = 0
        for id_, obj in self.objects.items():
            if isinstance(obj, cls):
                count += 1
                self.objects[id_].on_end(self)
                del self.objects[id_]
        return count

    def add_keyboard_listener(self):
        """Adds a keyboard listener, to fire events when a key is pressed.

        .. versionadded:: 0.0"""
        self.keyboard_listener = threading.Thread(target=_keyboard, args=(self,))
        self.keyboard_listener.start()

    def wait_until_key_released(self):
        """Waits until all keys are released.
        
        .. versionadded:: 0.1"""
        term = self.term
        with term.cbreak():
            while term.inkey(timeout=0.1) != "":
                pass
            
    def mspf(self) -> Union[Union[float, int], None]:
        """Gets the number of milliseconds per frame.
        
        .. versionadded:: 0.0

        :rtype: float or int or None"""
        if len(self.speeds) != 0: return sum(self.speeds)/len(self.speeds)
        return None

    def fps(self) -> Union[Union[float, int], None]:
        """Gets the number of frames per second.
        
        .. versionadded:: 0.0
        
        :rtype: float or int or None"""
        if len(self.speeds) != 0: avg_ms = sum(self.speeds)/len(self.speeds)
        else: return None
        if avg_ms == 0: return math.inf
        return round(1000 / avg_ms, 2)

    def get_displayed_pixel(self, x: int, y: int) -> Tuple[Optional[Tuple[int, int, int]], Optional[Tuple[int, int, int]], Optional[str]]:
        """Get the pixel at a certain global coordinate.
        
        .. versionadded:: 0.0
        
        :param int x: The global x coordinate of the pixel.
        :param int y: The global y coordinate of the pixel.
        :returns: A tuple of ``(back colour, fore colour, character)``
        :rtype: Tuple[Optional[Tuple[int, int, int]], Optional[Tuple[int, int, int]], Optional[str]]"""
        back, fore, char = (None,)*3
        values = list(self.objects.values())[:]
        for obj in values:
            lx, rx, ty, by = obj.edges()
            if x < lx or x > rx or y < ty or y > by: continue
            if issubclass(type(obj), Sprite):
                obj: Sprite # pacify linter
                pixel_info = obj.pixels[x-obj.x, y-obj.y]
                if 'back' in pixel_info.keys() and pixel_info['back'] is not None: back = pixel_info['back']
                if 'fore' in pixel_info.keys() and ['fore'] is not None: fore = pixel_info['fore']
                if 'char' in pixel_info.keys() and ['char'] is not None: char = pixel_info['char']
            elif issubclass(type(obj), Text):
                obj: Text # pacify linter
                pos = obj.get_char_positions()
                if (x-obj.x, y-obj.y) not in pos.keys(): continue
                if obj.back is not None: back = pixel._parse_colours(obj.back) # noqa
                if obj.fore is not None: fore = pixel._parse_colours(obj.fore) # noqa
                char = pos[x-obj.x, y-obj.y]
            else:
                continue
        return back, fore, char

    def handle_error(self):
        """Handles any error properly when the game is running.

        .. versionadded:: 0.0

        **Example:**

        .. code-block:: python

           try:
               game.start()
               ...
           except Exception as e:
               game.handle_error()
        """
        term = self.term
        self.game_on = False
        print(term.home + term.clear_eos + term.bright_red("An error has occured and the game will quit shortly.\n") + term.red(traceback.format_exc()))
        time.sleep(0.5)
        print(term.bright_red("Press any key to continue..."))
        with term.cbreak():
            term.inkey(timeout=15)
        

def _loop(game: Game):
    """:meta private:"""
    term = game.term
    try:
        while game.game_on:
            loop_start = time.time()
            for obj in game.objects.values():
                obj.pre_update(game)
            for obj in game.objects.values():
                obj.update(game)
            for obj in game.objects.values():
                obj.post_update(game)

            out = ""
            lx, rx, ty, by = game.screen.edges()
            for y in range(ty, by+1):
                for x in range(lx, rx+1):
                    back, fore, char = game.get_displayed_pixel(x, y)
                    back_style = (lambda o: o) if back is None else term.on_color_rgb(*back)
                    fore_style = (lambda o: o) if fore is None else term.color_rgb(*fore)
                    char = " " if char is None else char
                    out += back_style(fore_style(char))
            print(term.home + out + term.clear_eos, end="", flush=True)

            #print(term.home + str(game.fps()) + term.clear_eol, flush=True)
            game.speeds.append(1000*(time.time()-loop_start))
            if len(game.speeds) > 100: game.speeds.pop(0)
    except Exception:
        game.handle_error()

def _keyboard(game: Game):
    """:meta private:"""
    term = game.term
    try:
        while game.game_on:
            with term.cbreak():
                key = term.inkey(timeout=1)
                if key:
                    if game.current_text_input is None:
                        game.call_event("keyboard_press", key)
                    else:
                        game.current_text_input.on_keyboard_press(game, key)
    except Exception:
        game.handle_error()