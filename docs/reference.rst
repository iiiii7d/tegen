Reference
=========
.. py:currentmodule:: tegen

.. py:attribute:: __version__
   :type: str
   
   The version.

   Versions go in this format: **x.y.z**

   * **x**: Projects built for different x versions are incompatitable. If 'x' is 0, is is a development release.
   * **y**: Features have been added from the previous y version.
   * **z**: Minor bug fixes.

Game
----

.. autoclass:: Game
   :members:

Scene
-----

.. autoclass:: Scene
   :members:

Objects
-------

.. py:currentmodule:: tegen.objects

.. autoclass:: Object
   :members:

.. autoclass:: Screen
   :members:

.. autoclass:: Sprite
   :members:

.. autoclass:: Text
   :members:

.. autoclass:: TextInput
   :members:

Pixel Utils
-----------

.. py:currentmodule:: tegen.pixel

.. autofunction:: from_2d_array

.. autofunction:: from_image