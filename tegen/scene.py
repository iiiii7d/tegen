from tegen.objects import Screen, Object

class Scene:
    """A game scene.
    
    .. versionadded:: 0.0"""

    def __init__(self):
        self.objects = {}

    def add_object(self, obj: Object, id_: str, x: float, y: float):
        """Adds an :py:class:`Object` to the scene.
        
        .. versionadded:: 0.0
        
        :param Object obj: The object to add
        :param str id_: The ID to give to the object
        :param float x: The global x coordinate of the anchor (local x=0)
        :param float y: The global y coordinate of the anchor (local y=0)
        :raises ValueError: if one of the ``objs`` is a :py:class:`Screen`"""
        if isinstance(obj, Screen):
            raise ValueError("Object added cannot be a screen, access the screen via `Game.screen`")
        self.objects[id_] = {
            "obj": obj,
            "x": x,
            "y": y
        }

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
        for id_, v in self.objects.items():
            if isinstance(v['obj'], cls):
                del self.objects[id_]

        
