"""
objeto.py

RogueLike, object class and components.

  class Object  : base Object logic class

  class Fighter : fighter component

  class Item    : item component
"""

import logging
import math

log = logging.getLogger('roguelike.object')

class Object(object):
    """
    Object class.

    This is the base class for any object living in the World,
    defining things such as its position, color, etc.

    Methods:
      __init__
      move
      distance
      clear

    Variables:
      x, y     - coordinates in which the object 'lives' in the level
      char     - char to represent the object when rendered
      color    - color to use to render  the object
      name     - name of the object
      blocks   - whether the object blocks other objects or not
      curlevel - level at which this object is currently living
    """
    def __init__(self, char, color, name, x = -1, y = -1, curlevel = None, blocks = False,
                 fighter=None, ai=None, item=None):
        """
        Initialize object.

        Arguments:
          x,y      : coordinates in the level for the object
          char     : character representing the object
          color    : color to pain the character in screen
          name     : name to be used for description of the object
          curlevel : level at which object is currently living
          blocks   : whether the objects blocks the pass of
                     player/monsters or not (default: NO)
          fighter  : fighter component, if object is a
                     monster/player. Default: None
          ai       : ai component, if object is a monster. Default: None
          item     : item component, if object is a item. Default: None
        """
        (self.x, self.y) = (x,y)
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.curlevel = curlevel

        self.fighter = fighter
        self.ai = ai
        self.item = item

    def move(self, dx, dy):
        """Move object to (x+dx, y+dy)."""
        if not self.curlevel[0].is_blocked(self.x + dx, self.y + dy):
            self.x = self.x + dx
            self.y = self.y + dy

    def distance(self, x, y):
        """Distance to some coordinates."""
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def clear(self):
        """Clear object."""
        pass

class Fighter:
    """
    Fighter component class.

    This class should be composited in some monster or player Object
    to define that it can fight, be hitted, etc.
    """
    def __init__(self):
        pass

class Item:
    """
    Item component class.

    This class should be composited in some item Object to define that
    it can be picked, used, etc.
    """
    def __init__(self):
        pass
