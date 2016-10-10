# -*- coding: utf-8 -*-
"""
tile.py

RogueLike tiles for the maps.

  class TILETYPES    : holds dictionaries to define each type of tile a
                       map can have

  class Tile         : defines a tile in the map

"""


"""
Types for the tiles in the map.

Defines walls, floors, ...

Each type must have:
  name        - a name for the tile type
  char        - a character to represent the tile when drawn
  file_char   - a character to represent the tile when read from file, must be unique
  just_color  - print just the color, some uiwrappers may want to draw this as the color alone, not the char
  color       - the color of the char when drawn
  nv_color    - the color to use for the tile when drawn in 'not
                being viewed' (by the player) mode
  block_pass  - tells if the tile will block passage for
                players/monsters
  block_sight - tells if the tile will block line of sight for
                players/monsters
"""
TILETYPES = {
    # Walls
    'air'    : {'name'     : 'air',
              'char'       : u' ',
              'file_char'  : u' ',
              'just_color' : False,
              'color'      : 'dark_grey',
              'nv_color'   : 'black',
              'block_pass' : True,
              'block_sight': False},

    'ow_air': {'name'      : 'overwaterair',
              'char'       : u' ',
              'file_char'  : u'`',
              'just_color' : False,
              'color'      : 'dark_blue',
              'nv_color'   : 'black',
              'block_pass' : True,
              'block_sight': False},

    'rock'   : {'name'     : 'rock',
              'char'       : u' ',
              'file_char'  : u',',
              'just_color' : True,
              'color'      : 'black',
              'nv_color'   : 'black',
              'block_pass' : True,
              'block_sight': True},

    'wall'   : {'name'     : 'wall',
              'char'       : u'#',
              'file_char'  : u'#',
              'just_color' : True,
              'color'      : 'darker_red',
              'nv_color'   : 'darkest_red',
              'block_pass' : True,
              'block_sight': True},

    'fence' : {'name'      : 'fence',
              'char'       : u'#',
              'file_char'  : u'|',
              'just_color' : True,
              'color'      : 'grey',
              'nv_color'   : 'dark_grey',
              'block_pass' : True,
              'block_sight': False},

    'tree'   : {'name'     : 'tree',
              'char'       : u'T',
              'file_char'  : u'T',
              'just_color' : False,
              'color'      : 'darker_green',
              'nv_color'   : 'darkest_green',
              'block_pass' : True,
              'block_sight': True},

    'window' : {'name'     : 'window',
              'char'       : u'=',
              'file_char'  : u'=',
              'just_color' : False,
              'color'      : 'light_cyan',
              'nv_color'   : 'darker_cyan',
              'block_pass' : True,
              'block_sight': False},

    'curtained_window' : {'name'     : 'window',
                          'char'       : u'=',
                          'file_char'  : u'[',
                          'just_color' : False,
                          'color'      : 'light_cyan',
                          'nv_color'   : 'darker_cyan',
                          'block_pass' : True,
                          'block_sight': True},

    'closeddoor' : {'name' : 'door',
              'char'       : u'+',
              'file_char'  : u'+',
              'just_color' : False,
              'color'      : 'dark_grey',
              'nv_color'   : 'darkest_grey',
              'block_pass' : True,
              'block_sight': True},

    'opendoor' : {'name'   : 'door',
              'char'       : u'-',
              'file_char'  : u'*',
              'just_color' : False,
              'color'      : 'dark_grey',
              'nv_color'   : 'darkest_grey',
              'block_pass' : False,
              'block_sight': True},

    # Floors
    'dung_floor'  : {'name'     : 'floor',
                   'char'       : u'.',
                   'file_char'  : u'.',
                   'just_color' : True,
                   'color'      : 'light_grey',
                   'nv_color'   : 'darker_grey',
                   'block_pass' : False,
                   'block_sight': False},

    'floor'     : {'name'       : 'floor',
                   'char'       : u'.',
                   'file_char'  : u'_',
                   'just_color' : True,
                   'color'      : 'dark_grey',
                   'nv_color'   : 'black',
                   'block_pass' : False,
                   'block_sight': False},

    'grass'      : {'name'      : 'grass',
                   'char'       : u'.',
                   'file_char'  : u'^',
                   'just_color' : True,
                   'color'      : 'dark_green',
                   'nv_color'   : 'darkest_green',
                   'block_pass' : False,
                   'block_sight': False},

    'furniture' : {'name'       : 'furniture',
                   'char'       : u'-',
                   'file_char'  : u'%',
                   'just_color' : True,
                   'color'      : 'darker_yellow',
                   'nv_color'   : 'darkest_yellow',
                   'block_pass' : False,
                   'block_sight': True},

    # 'stall'       : {'name'       : 'stall',
    #                'char'       : u'-',
    #                'file_char'  : u'_',
    #                'just_color' : False,
    #                'color'      : 'dark_yellow',
    #                'nv_color'   : '',
    #                'block_pass' : False,
    #                'block_sight': False},

    # 'desk'        : {'name'       : 'desk',
    #                'char'       : u'-',
    #                'file_char'  : u'-',
    #                'just_color' : False,
    #                'color'      : 'dark_yellow',
    #                'nv_color'   : '',
    #                'block_pass' : False,
    #                'block_sight': False},

    'water'       : {'name'     : 'water',
                   'char'       : u'~',
                   'file_char'  : u'~',
                   'just_color' : True,
                   'color'      : 'cyan',
                   'nv_color'   : 'blue',
                   'block_pass' : True,
                   'block_sight': False},

    # Stairs
    'stairs' : {'name'     : 'stairs',
              'char'       : u'<',
              'file_char'  : u'X',
              'just_color' : False,
              'color'      : 'darkest_amber',
              'nv_color'   : 'darkest_crimson',
              'block_pass' : False,
              'block_sight': False},

    # Special
    'initpoint' : {'name'  : 'initpoint',
              'char'       : u'<',
              'file_char'  : u'h',
              'just_color' : False,
              'color'      : 'green',
              'nv_color'   : 'darkest_lime',
              'block_pass' : False,
              'block_sight': False},

    'special' : {'name'    : 'special',
              'char'       : u'?',
              'file_char'  : u'?',
              'just_color' : False,
              'color'      : 'red',
              'nv_color'   : 'black',
              'block_pass' : False,
              'block_sight': False},
    }

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
    def __init__(self, tipo = 'wall'):
        """
        Initializes a tile.

        Arguments:
          tipo - the type of the tile. Default: TILETYPES.wall
        """
        self.tipo     = tipo
        # 'explored by the player' status
        self.explored = False
