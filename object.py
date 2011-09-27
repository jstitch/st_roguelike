"""
object.py

RogueWarts, object class and components.

  class Object  : base Object model class

  class Fighter : fighter component

  class Item    : item component
"""

import logging
import math

log = logging.getLogger('roguewarts.object')

class Object:
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
    def __init__(self, char, color, name, x = -1, y = -1, blocks = False,
                 fighter=None, ai=None, item=None):
        """
        Initialize object.

        Arguments:
          x,y     : coordinates in the level for the object
          char    : character representing the object
          color   : color to pain the character in screen
          name    : name to be used for description of the object
          blocks  : whether the objects blocks the pass of
                    player/monsters or not (default: NO)
          fighter : fighter component, if object is a monster/player
          ai      : ai component, if object is a monster
          item    : item component, if object is a item
        """
        (self.x, self.y) = (x,y)
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.curlevel = None

    def move(self, dx, dy):
        """Move object to (x+dx, y+dy)."""
        if not self.curlevel.is_blocked(self.x + dx, self.y + dy):
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
