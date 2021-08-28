from typing import Union, Tuple, Optional, Dict, List
import blessed
import threading
import time
import math
import traceback

from tegen.scene import Scene
from tegen.objects import Screen, Sprite, Object

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
       
    .. py:attribute:: objects
       :type: Dict[object, dict]
       
       A list of objects currently loaded.
       
       .. versionadded:: 0.0"""
    
    term = blessed.Terminal()

    def __init__(self):
        self.game_on = False
        self.loop: threading.Thread = None
        self.keyboard_listener: threading.Thread = None
        self.objects: Dict[tuple, Object] = {}
        self.screen = Screen(0, 0)
        self.current_scene: Scene = None
        self.speeds: List[float] = []

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

    def call_event(self, event: str, *args, **kwargs):
        """Calls an event, running `on_<event name>` in all :py:class:`Object` s, if present.
        
        .. versionadded:: 0.0
        
        :param str event: The name of the event to call"""
        def empty():
            pass
        
        for id_, obj in self.objects.items():
            getattr(obj, 'on_'+event, empty)(self, *args, **kwargs) # noqa

    def add_keyboard_listener(self):
        """Adds a keyboard listener, to fire events when a key is pressed.

        .. versionadded:: 0.0"""
        self.keyboard_listener = threading.Thread(target=_keyboard, args=(self,))
        self.keyboard_listener.start()
            
    def mspf(self) -> Union[Union[float, int], None]:
        """Gets the number of milliseconds per frame.
        
        .. versionadded:: 0.0

        :rtype: float or int or None"""
        if len(self.speeds) != 0: return sum(self.speeds)/len(self.speeds)
        else: return None

    def fps(self) -> Union[Union[float, int], None]:
        """Gets the number of frames per second.
        
        .. versionadded:: 0.0
        
        :rtype: float or int or None"""
        if len(self.speeds) != 0: avg_ms = sum(self.speeds)/len(self.speeds)
        else: return None
        if avg_ms == 0: return math.inf
        else: return round(1000 / avg_ms, 2)

    def get_displayed_pixel(self, x: int, y: int) -> Tuple[Optional[Tuple[int, int, int]], Optional[Tuple[int, int, int]], Optional[str]]:
        """Get the pixel at a certain global coordinate.
        
        .. versionadded:: 0.0
        
        :param int x: The global x coordinate of the pixel.
        :param int y: The global y coordinate of the pixel.
        :returns: A tuple of ``(back colour, fore colour, character)``
        :rtype: Tuple[Optional[Tuple[int, int, int]], Optional[Tuple[int, int, int]], Optional[str]]"""
        back, fore, char = (None,)*3
        for obj in self.objects.values():
            lx, rx, ty, by = obj.edges()
            if x < lx or x > rx or y < ty or y > by: continue
            if not issubclass(type(obj), Sprite): continue
            obj: Sprite # pacify linter
            pixel_info = obj.pixels[(x-obj.x, y-obj.y)]
            if 'back' in pixel_info.keys() and pixel_info['back'] is not None: back = pixel_info['back']
            if 'fore' in pixel_info.keys() and ['fore'] is not None: fore = pixel_info['fore']
            if 'char' in pixel_info.keys() and ['char'] is not None: char = pixel_info['char']
        return back, fore, char

    def handle_error(self):
        """Handles any error properly when the game is running.

        .. versionadded:: 0.0

        **Example:**

        .. code-block:: python

           game.start()
           try:
               ...
           except Exception as e:
               game.handle_error()
        """
        term = self.term
        self.game_on = False
        print(term.home + term.bright_red("An error has occured and the game will quit shortly.\n") + term.red(traceback.format_exc()) + term.eos)
        print(term.bright_red("Press any key to continue..."), flush=True)
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
            print(term.home + out + term.eos, end="", flush=True)

            print(term.home + str(game.fps()) + term.eol, flush=True)
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
                key = term.inkey()
                game.call_event("keyboard_press", key)
    except Exception:
        game.handle_error()