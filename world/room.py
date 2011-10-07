"""
room.py

RogueWarts rooms for a map.

Figure classes use ducktyping to give a common interface to map
methods.

Coordinates in this classes are relative to the map ones.

  class Rect         : base class for rectangular rooms

  class Circle       : base class for circular rooms

  class Hexag        : base class for hexagonal rooms

TODO:
  - implement classes for geometrics different from the Rect one.
"""

class Rect:
    """
    Rectangle, basic unit for rooms, class.

    Methods:
      __init__
      center
      intersect

    Variables:
      (x1,y1) - top left corner coordinates of the rectangle
      (x2,y2) - bottom right corner coordinates of the rectangle
    """
    def __init__(self, (x, y), (w, h)):
        """
        Initializes rooms size with given coordinates.

        Arguments:
          (x, y) : coordinates for top left corner of the room
          (w, h) : size of the room
        """
        (self.x1, self.y1) = (x, y)
        (self.x2, self.y2) = (x + w, y + h)

    def center(self):
        """
        Get center coordinates.

        Returns:
          tuple with int coordinates of the center of the room
        """
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, other):
        """
        Determines if this room intersects with any other.

        Arguments:
          other - some other room

        Returns:
          boolean, true if this room intersects with another room.

        TODO:
          - currently just supports intersection between rectangular
            rooms.
        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class Circle:
    """
    Circle, basic unit for rooms, class.

    Methods:
      __init__
      center
      intersect

    Variables:
    """
    def __init__():
        """
        Initializes rooms properties.
        """
        pass

    def center(self):
        """
        Get center coordinates.

        Returns:
          tuple with int coordinates of the center of the room
        """
        pass

    def intersect(self, other):
        """
        Determines if this room intersects with any other.

        Arguments:
          other - some other room

        Returns:
          boolean, true if this room intersects with another room.
        """
        pass

class Hexag:
    """
    Hexagone, basic unit for rooms, class.

    Methods:
      __init__
      center
      intersect

    Variables:
    """
    def __init__():
        """
        Initializes rooms properties.
        """
        pass

    def center(self):
        """
        Get center coordinates.

        Returns:
          tuple with int coordinates of the center of the room
        """
        pass

    def intersect(self, other):
        """
        Determines if this room intersects with any other.

        Arguments:
          other - some other room

        Returns:
          boolean, true if this room intersects with another room.
        """
        pass
