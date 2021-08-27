import blessed
import threading
import time
import math
from typing import Union

from tegen.scene import Scene
from tegen.objects import Screen

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
            getattr(v['obj'], 'on_'+event, default=empty)()
            
    def mspl(self) -> Union[Union[float, int], None]:
        """Gets the number of milliseconds per loop.
        
        .. versionadded:: 0.0

        :rtype: float or int or None"""
        if len(self.speeds) != 0: return sum(self.speeds)/len(self.speeds)
        else: return None

    def lps(self) -> Union[Union[float, int], None]:
        """Gets the number of loops per second.
        
        .. versionadded:: 0.0
        
        :rtype: float or int or None"""
        if len(self.speeds) != 0: avg_ms = sum(self.speeds)/len(self.speeds)
        else: return None
        if avg_ms == 0: return math.inf
        else: return round(1000 / avg_ms, 2)

    def get_displayed_pixel(self, x: int, y: int):
        """Get the pixel at a certain global coordinate.
        
        .. versionadded:: 0.0
        
        :param int x: The global x coordinate of the pixel.
        :param int y: The global y coordinate of the pixel."""
        lx, rx, ty, by = self.screen.edges()
        for data in self.objects.values():
            pass



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
        print(term.home + str(game.lps()) + term.eol, flush=True)
        game.speeds.append(1000*(time.time()-loop_start))
        if len(game.speeds) > 100: game.speeds.pop(0)