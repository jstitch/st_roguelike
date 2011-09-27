"""
room.py

RogueWarts rooms for a map.

Figure classes use ducktyping to give a common interface to map
methods.

Coordinates in this classes are relative to the map ones.

  class Rect         : base class for rectangular rooms

  class Circle       : base class for circular rooms

  class Hexag        : base class for hexagonal rooms

  class TILETYPES    : holds dictionaries to define each type of tile a
                       map can have

  class Tile         : defines a tile in the map
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

        TODO: currently just supports intersection between rectangular
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

class TILETYPES:
    """
    Types for the tiles in the map.

    Defines walls, floors, ...

    Each type must have:
      name        - a name for the tile type
      char        - a character to represent the tile when drawn
      color       - the color of the char when drawn
      nv_color    - the color to use for the tile when drawn in 'not
                    being viewed' (by the player) mode
      block_pass  - tells if the tile will block passage for
                    players/monsters
      block_sight - tells if the tile will block line of sight for
                    players/monsters
    """
    # Walls
    wall   = {'name'       : 'wall',
              'char'       : '#',
              'color'      : 'dark_blue',
              'nv_color'   : '',
              'block_pass' : True,
              'block_sight': True}

    tree   = {'name'       : 'tree',
              'char'       : '#',
              'color'      : 'dark_green',
              'nv_color'   : '',
              'block_pass' : True,
              'block_sight': True}

    window = {'name'       : 'window',
              'char'       : '=',
              'color'      : 'light_cyan',
              'nv_color'   : '',
              'block_pass' : True,
              'block_sight': False}

    # Floors
    dung_floor  = {'name'       : 'floor',
                   'char'       : '.',
                   'color'      : 'light_yellow',
                   'nv_color'   : '',
                   'block_pass' : False,
                   'block_sight': False}

    stall       = {'name'       : 'stall',
                   'char'       : '-',
                   'color'      : 'dark_yellow',
                   'nv_color'   : '',
                   'block_pass' : False,
                   'block_sight': False}

    desk        = {'name'       : 'desk',
                   'char'       : '-',
                   'color'      : 'dark_yellow',
                   'nv_color'   : '',
                   'block_pass' : False,
                   'block_sight': False}

class Tile:
    """
    Tile class, a tile on the map.

    Methods:
      __init__

    Variables:
      tipo     - the type for the tile (from room.TILETYPES)
      explored - says if this tile has already been explored by the
                 player (and so it must be drawn if true, or not if
                 false (fog of war))

    Given the explored flag, notice how EVERY player of the game will
    see and have explored anything other players already have. If
    playing alone, this may sound good, or not, depending on the game
    itself. Maybe some work must be done to have each player store
    this information, instead of the tile, in case different FOGs are
    required, one for each player.
    """
    def __init__(self, tipo = TILETYPES.wall):
        """
        Initializes a tile.

        Arguments:
          tipo - the type of the tile. Defaults to a wall
        """
        self.tipo = tipo
        # 'explored by the player' status
        self.explored = False
