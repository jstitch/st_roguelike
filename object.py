"""
object.py

RogueWarts, object class

This is the base class for any object living in the World, defining
things such as its position, color, etc.

  class Object : base Object class
"""

import logging
import math

log = logging.getLogger('roguewarts.object')

class Object:
    """
    Object class.

    Methods:
      __init__
      move
      distance
      clear

    Variables:
      x, y
      char
      color
      name
      blocks
    """
    def __init__(self, x = -1, y = -1, char, color, name, blocks = False):
        """
        Initialize object.

        Arguments:
          x,y    : coordinates in the level for the object
          char   : character representing the object
          color  : color to pain the character in screen
          name   : name to be used for description of the object
          blocks : whether the objects blocks the pass of
                   player/monsters or not (default: NO)
        """
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        """Move object to (x+dx, y+dy)."""
        self.x = self.x + dx
        self.y = self.y + dy

    def distance(self, x, y):
        """Distance to some coordinates."""
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def clear(self):
        """Clear object."""
        pass
