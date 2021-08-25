from tegen.objects import Screen, Object
from typing import Tuple

class Scene:
    """A game scene.
    
    .. versionadded:: 0.0"""

    def __init__():
        self.objects = {}
        self.screen_position = (0, 0)

    def add_objects(self, *objs: Object):
        """Adds :py:class:`Object`s to the scene.
        
        .. versionadded:: 0.0
        
        :param Object objs: The objects to add
        :raises ValueError: if one of the ``objs`` is a :py:class:`Screen`"""
        for obj in objs:
            if isinstance(obj, Screen):
                raise ValueError("Object added cannot be a screen, access the screen via `Game.screen`")
            self.objects[obj] = {}

    def remove_object(self, *objs: Object, nonexist_error: bool=False):
        """Removes :py:class:`Object`s from the scene.

        .. versionadded:: 0.0

        :param bool nonexist_error: Whether to raise an error if an object does not exist in the scene."""
        for obj in objs:
            try:
                del self.objects[obj]
            except KeyError as e:
                if nonexist_error: raise e
