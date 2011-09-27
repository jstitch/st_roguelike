"""
level.py

RogueWarts level definition.

Defines a level and its properties, inside the world.

  map MAX_ROOM_OBJECTS : how many generated objects allowed in
                         room. Dictionary with keys for each type of
                         object (currentlye monsters and items)

  class Level          : each world is composed of levels, this is one
"""

import libtcod.libtcodpy as tcod
import logging
import time, calendar
import mapa
import util

log = logging.getLogger('roguewarts.level')

"""Maximum number of objects to be generated in a given room, by type"""
MAX_ROOM_OBJECTS = {'monster': 3, 'item': 2}

class Level:
    """
    A level in the world class.
    
    Methods:
      __init__
      place_objects

    Variables:
      objects      - list of objects currently living in the level
                     (object = monster/player/item)
      players      - list of players currently playing in the level
      numlevel     - id number for the level
      name         - common name for the level
      ismaraudable - tells if this level can be displayed in a
                     Marauder's map
      branch       - The world's branch to which the level belongs
      mapa         - The associated map of the level
    """
    def __init__(self, numlevel, name, branch, rng):
        """
        Initialize the level.

        -A new level is 'empty' (has no objects).
        -A new level must have an id (numlevel) and a name.
        -A new level must belong to a given world's branch.
        -A new level must have an associated map.

        Given a branch, the type of map to be associated must be
        decided. Right now the rules for deciding this are HARD-CODED,
        must do this in another way... (some kind of config file? some
        kind of class or structure holding this rules?).

        Also, this rules defines, in a way, the complete structure of
        the world (where each branch begins and ends). This info
        should be delivered by the World itself, in not-hard-coded
        rules too.
        """
        self.objects = []
        self.players = []
        self.numlevel = numlevel
        self.name = name
        self.ismaraudable = False
        self.branch = branch

        if self.branch['name'] == 'classrooms':
            maptype = self.branch['maptypes'][0] if numlevel < 5 else self.branch['maptypes'][1]

        elif self.branch['name'] == 'dungeons':
            maptype = self.branch['maptypes'][0] if numlevel > -5 else self.branch['maptypres'][1]

        elif self.branch['name'] == 'woods':
            maptype = self.branch['maptypes'][0]

        if numlevel > 10 or numlevel < -10:
            maptype = mapa.MAPTYPES.labyrinth

        # debugging dungeons, remove True or condition
        if util.debug or True:
            maptype=mapa.MAPTYPES.dungeon2

        self.mapa = getattr(mapa, maptype['name'])(maptype, rng)

    def place_objects(self):
        """
        Place random objects in level.
        """
        pass
