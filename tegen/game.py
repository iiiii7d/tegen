import blessed
import threading
import time
import math
from typing import Union, Tuple, Optional

from tegen.scene import Scene
from tegen.objects import Screen, Sprite

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
        self.loop = None
        self.objects = {}
        self.screen = Screen(0, 0)
        self.current_scene = None
        self.speeds = []

    def start(self, show_info=True):
        """Starts the game.

        .. versionadded:: 0.0

        :param bool show_info: Whether to show tegen and terminal info before the game starts"""
        term = self.term
        print(term.height*"\n")
        print(term.home + term.clear, end='')
        if show_info:
            from tegen import __version__
            print(term.bold("tegen v"+__version__))
            print("number of colours: "+str(term.number_of_colors))
            print("terminal size (h,w): "+str((term.height, term.width)))
            time.sleep(3)
        print(term.home + term.clear, end='')
        self.game_on = True
        self.loop = threading.Thread(target=_loop, args=(self,))
        self.loop.start()
        
    def end(self):
        """Ends the game.

        .. versionadded:: 0.0"""
        term = self.term
        for id_, v in self.objects.items():
            v['obj'].on_end(self)
        self.game_on = False
        print(term.home + term.clear, end='')

    def load_scene(self, scene: Scene, clear_objects: bool=True):
        """Loads a scene to the game.

        .. versionadded:: 0.0

        :param Scene scene: The scene to load
        :param bool clear_objects: Whether to clear all objects in the previous scene before loading the new scene"""
        for id_, v in self.objects.items():
            v['obj'].on_end(self)
        self.current_scene = scene
        if clear_objects: self.objects.clear()
        self.objects.update(scene.objects)
        for id_, v in self.objects.items():
            v['obj'].on_init(self)

    def call_event(self, event: str):
        """Calls an event, running `on_<event name>` in all :py:class:`Object` s, if present.
        
        .. versionadded:: 0.0
        
        :param str event: The name of the event to call"""
        def empty():
            pass
        
        for id_, v in self.objects.items():
            getattr(v['obj'], 'on_'+event, __default=empty)()
            
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
        for data in self.objects.values():
            lx, rx, ty, by = data['obj'].edges(data['x'], data['y'])
            if x < lx or x > rx or y < ty or y > by: continue
            if not issubclass(type(data['obj']), Sprite): continue
            pixel_info = data['obj'].pixels[(x-data['x'], y-data['y'])]
            if back is not None: back = pixel_info[back]
            if fore is not None: fore = pixel_info[fore]
            if char is not None: char = pixel_info[char]
        return back, fore, char

def _loop(game: Game):
    """:meta private:"""
    term = game.term
    while game.game_on:
        loop_start = time.time()
        for obj in game.objects.values():
            obj['obj'].pre_update(game)
        for obj in game.objects.values():
            obj['obj'].update(game)
        for obj in game.objects.values():
            obj['obj'].post_update(game)

        out = ""
        lx, rx, ty, by = game.screen.edges()
        for y in range(ty, by+1):
            for x in range(lx, rx+1):
                back, fore, char = game.get_displayed_pixel(x, y)
                back_style = (lambda o: o) if back is None else term.on_color_rgb(*back)
                fore_style = (lambda o: o) if fore is None else term.color_rgb(*fore)
                char = " " if char is None else char
                out += back_style(fore_style(char))
        breakpoint()
        #print(term.home + out + term.eos, end="", flush=True)

        #print(term.home + str(game.fps()) + term.eol, flush=True)
        game.speeds.append(1000*(time.time()-loop_start))
        if len(game.speeds) > 100: game.speeds.pop(0)