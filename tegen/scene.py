from typing import Dict

from tegen.objects import Screen, Object

class Scene:
    """A game scene.
    
    .. versionadded:: 0.0
    
    .. py:attribute:: objects
       :type: Dict[str, Object]
       
       A dict of objects, in the form of ``{id: object}``"""

    def __init__(self):
        self.objects: Dict[str, Object] = {}

    def add_object(self, obj: Object, id_: str, x: float, y: float, override: bool=False):
        """Adds an :py:class:`Object` to the scene.
        
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

    def remove_object_by_id(self, id_: str, nonexist_error: bool=False):
        """Removes an :py:class:`Object` from the scene by its ID.

        .. versionadded:: 0.0

        :param str id_: The ID of the object to remove
        :param bool nonexist_error: Whether to raise an error if an object does not exist in the scene."""
        try:
            del self.objects[id_]
        except KeyError as e:
            if nonexist_error: raise e

    def remove_object_by_class(self, cls: type):
        """Removes :py:class:`Object` s from the scene by their class type.
        
        .. versionadded:: 0.0
        
        :param type cls: The class, should be a subclass of :py:class:`Object`
        :raises TypeError: if the class is not a subclass of :py:class:`Object`"""
        if not issubclass(cls, Object):
            raise TypeError("Class is not subclass of Object")
        for id_, obj in self.objects.items():
            if isinstance(obj, cls):
                del self.objects[id_]

        
