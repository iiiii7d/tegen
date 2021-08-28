from typing import List, Optional, Union, Tuple, Dict
import re
from PIL import Image

PixelMap = Dict[tuple, Dict[str, Union[str, Tuple[int, int, int]]]]

def _parse_colours(colour: Optional[Union[Union[int, str], Union[tuple, list]]]) -> Optional[Tuple[int, int, int]]:
    """:meta private:"""
    if colour is None: return None
    if isinstance(colour, (list, tuple)):
        if len(colour) != 3:
            raise ValueError(f"Colour sequence must have 3 values (Got {colour})")
        return tuple(colour)
    if isinstance(colour, str):
        m = re.search(r"^#?([0-9a-f]{6}|[0-9a-f]{3})$", colour)
        if m is None:
            raise ValueError(f"Invalid hex code")
        hexc = m.group(1)
        if len(hexc) == 3: hexc = 2*hexc[0]+2*hexc[1]+2*hexc[2]
        return int(hexc[0:2], base=16), int(hexc[2:4], base=16), int(hexc[4:6], base=16)
    else:
        hexc = hex(colour)[2:]
        return int(hexc[0:2], base=16), int(hexc[2:4], base=16), int(hexc[4:6], base=16)

def _find_origin(order: Tuple[int, int], anchor: str):
    """:meta private:"""
    lx, ty = (float("inf"),) * 2
    rx, by = (0,) * 2
    for y in range(order[1]):
        for x in range(order[0]):
            if x > rx: rx = x
            if x < lx: lx = x
            if y > by: by = y
            if y < ty: ty = y
    if anchor == "center":
        ox = round((lx + rx) / 2)
        oy = round((ty + by) / 2)
    else:
        if anchor not in ['tr', 'tl', 'br', 'bl']:
            raise ValueError("'anchor' is not one of 'center', 'tr', 'tl', 'br', 'bl'")
        ox = lx if anchor[1] == 'l' else rx
        oy = ty if anchor[0] == 't' else by
    return ox, oy

def from_2d_array(back: Optional[List[List[str]]]=None, fore: Optional[List[List[str]]]=None,
                  char: Optional[List[str]]=None, anchor: str='tr') -> PixelMap:
    """Generates a map of pixels from 2d arrays.

    .. versionadded:: 0.0

    :param List[List[str]] back: A list of lists of colours as the background
    :param List[List[str]] fore: A list of lists of colours as the foreground
    :param List[str] char: A list of strings as rows as the characters
    :param str anchor: The corner to set the local coordinate as ``(0, 0)``, choose from ``tr``, ``tl``, ``br``, ``bl``, ``center``
    :rtype: PixelMap
    :raises ValueError: if ``back``, ``fore``, or ``char`` has no columns, or is a list of empty rows
    :raises ValueError: if ``back``, ``fore``, or ``char`` has inconsistent lengths of rows
    :raises ValueError: if ``back``, ``fore``, or ``char`` have inconsistent array sizes"""

    #check for equal order of lists
    order = (0, 0)
    prev = ""
    if char is not None: char = [list(s) for s in char]
    for name, a in [('back', back), ('fore', fore), ('char', char)]:
        if a is None: continue
        if len(a) == 0:
            raise ValueError(f"Parameter {name} has no columns, perhaps change it to 'None'?")
        orders = [len(l) for l in a]
        if any(x != orders[0] for x in orders):
            raise ValueError(f"Inconsistent length of rows for parameter {name}")
        if orders[0] == 0:
            raise ValueError(f"Parameter {name} is made of columns of no elements, perhaps change it to 'None'?")
        this_order = (len(a), orders[0])
        if order == (0, 0):
            order = this_order
            prev = name
        elif order != this_order:
            raise ValueError(f"Inconsistent sizes of arrays: {prev} is of size {order} but {name} is of size {this_order}")
        else:
            order = this_order
            prev = name

    # find anchor
    ox, oy = _find_origin(order, anchor)

    result = {}
    for name, a in [('back', back), ('fore', fore), ('char', char)]:
        if a is None: continue
        for y, yv in enumerate(a):
            for x, xv in enumerate(yv):
                if not (x-ox+2, y-oy) in result.keys(): result[(x-ox+2, y-oy)] = {}
                v = xv if name == 'char' else _parse_colours(xv)
                if isinstance(v, str) and v.strip() == '': v = None
                result[(x-ox+2, y-oy)][name] = v
    return result

def from_image(fp: str, anchor: str='tr', layer: str='fore', char: str='█') -> PixelMap:
    """Generates a map of pixels from an image. Each pixel in the image represents one character in the terminal.

    :param str fp: The file path of the image
    :param str anchor: The corner to set the local coordinate as ``(0, 0)``, choose from ``tr``, ``tl``, ``br``, ``bl``, ``center``
    :param str layer: The layer to write the pixels to, choose from ``back``, ``fore``
    :param str char: The character to serve as the single pixel
    :rtype: PixelMap
    :raises ValueError: if ``layer`` is not ``back`` or ``fore``
    :raises ValueError: if ``char`` is not 1 character long"""
    if layer not in ['back', 'fore']:
        raise ValueError("'layer' is not 'back' or 'fore'")
    if len(char) != 1:
        raise ValueError("'char' is not 1 character long")
    i = Image.open(fp)
    pmap = i.load()
    result = {}
    ox, oy = _find_origin(i.size, anchor)
    for x in range(i.size[0]):
        for y in range(i.size[1]):
            # pmap[x, y]
            result[(x-ox+2, y-oy)][layer] = pmap[x, y]
            result[(x-ox+2, y-oy)]['char'] = char
    return result