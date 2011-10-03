"""
tile.py

RogueWarts tiles for the maps.

  class TILETYPES    : holds dictionaries to define each type of tile a
                       map can have

  class Tile         : defines a tile in the map

"""

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
    air    = {'name'       : 'air',
              'char'       : ' ',
              'color'      : 'dark_gray',
              'nv_color'   : '',
              'block_pass' : True,
              'block_sight': False}

    rock   = {'name'       : 'rock',
              'char'       : ' ',
              'color'      : 'black',
              'nv_color'   : '',
              'block_pass' : True,
              'block_sight': True}

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

    # Stairs
    stairs = {'name'       : 'stairs',
              'char'       : '<',
              'color'      : 'light_green',
              'nv_color'   : '',
              'block_pass' : False,
              'block_sight': False}

class Tile:
    """
    Tile class, a tile on the map.

    Methods:
      __init__

    Variables:
      tipo     - the type for the tile (from tile.TILETYPES)
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
          tipo - the type of the tile. Default: TILETYPES.wall
        """
        self.tipo = tipo
        # 'explored by the player' status
        self.explored = False
