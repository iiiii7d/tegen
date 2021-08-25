from typing import List
PixelMap = dict

def from_2d_array(arr: List[List[str]], anchor: str='tr') -> PixelMap:
    """Geneerates a map of pixels from a 2d array.

    .. versionadded:: 0.0

    :param List[List[str]] arr: The array as the input
    :param str anchor: The corner to set the local coordinate as ``(0, 0)``, choose from ``tr``, ``tl``, ``br``, ``bl``
    :rtype: PixelMap"""
    # TODO: functionality for anchors
    result = {}
    for y, yv in enum(arr):
        for x, xv in enum(xv):
            result[(x, y)] = yv
    return result