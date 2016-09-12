# -*- coding: utf-8 -*-
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
import game.util as util
from tile import TILETYPES

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

    TODO:
      - make __str__ method to print the level as a map with objects
        (perhaps returning a tile.Tile array)
    """
    def __init__(self, numlevel, name, branch, rng):
        """
        Initialize the level.

        -A new level is 'empty' (has no objects).
        -A new level must have an id (numlevel) and a name.
        -A new level must belong to a given world's branch.
        -A new level must have an associated map.

        Given a branch, the type of map to be associated must be
        decided.

        Arguments:
          numlevel - the level id number
          name     - the generic name for the level
          branch   - the branch in the world to which this level belongs
          rng      - the world's random number generator

        TODO:
          - Right now the rules for deciding the type of map to
            associate the level on a given branch are HARD-CODED, must
            do this in another way... (some kind of config file?  some
            kind of class or structure holding this rules?).  Also,
            this rules defines, in a way, the complete structure of
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

        elif self.branch['name'] == 'from_file':
            maptype = self.branch['maptypes'][0]
            maptype['makeparams']['numlevel'] = numlevel

        if numlevel > 10 or numlevel < -10:
            maptype = mapa.MAPTYPES.labyrinth

        # debugging dungeons, remove True or condition
        if util.debug:
            maptype=mapa.MAPTYPES.dungeon2

        self.mapa = getattr(mapa, maptype['name'])(maptype, rng)

    def is_blocked(self, x, y):
        """
        Determines if coordinates in level are blocked for movement.

        Blocking occurs if tile type is defined as blocking, or if
        object at coordinates blocks too.

        Returns:
          Boolean indicating if coordinates are blocked for movement.
        """
        if TILETYPES[self.mapa.mapa[x][y].tipo]['block_pass'] == True:
            return True

        for objeto in self.objects:
            if objeto.blocks and objeto.x == x and objeto.y == y:
                return True

        return False

    def place_objects(self):
        """
        Place random objects in level.
        """
        pass
