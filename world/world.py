# -*- coding: utf-8 -*-
"""
world.py

RogueWarts world.

The World holds all the game information which is not related to the
UI or to the way the game evolves through time (which belongs to the
engine). Ie, it holds all the game data and its current state.

Note that there can be any number of 'players' in the world. This not
necessarily means that there will be a lot of users playing the same
game. The players in the world are just a number of characters which a
single user may handle in turns during the game. As if playing with
several characters at once. It may also mean several users for the
game, but RogueWarts is not conceived with this idea in mind. Several
tasks should be accomplished before implementing a multi-user game:
right now there's only one FogOfWar for every player (so what one
player discovers, the other players also see); also, right now the UI
is implemented for a single terminal, perhaps some UI for several
terminals taking turns (via a network or something) should be needed
for a multi-user game.

  class World         : the world logic class

  class WORLDBRANCHES : the branches on which the levels are grouped
"""

import libtcod.libtcodpy as tcod
import logging
import time, calendar

import level
import mapa
import objects.player as player

log = logging.getLogger('roguewarts.world')

class WORLDBRANCHES:
    """
    Branches of the world.

    Each branch is a dictionary with the following structure:

      - name     : the generic name for the branch

      - maptypes : a list containing mapa.MAPTYPES, giving the valid
                   map types that any level in the branch may hold
    """
    classrooms = {'name'    : 'classrooms',
                  'maptypes': [mapa.MAPTYPES.classrooms, mapa.MAPTYPES.classrooms2]}

    dungeons   = {'name'    : 'dungeons',
                  'maptypes': [mapa.MAPTYPES.dungeon, mapa.MAPTYPES.dungeon2]}

    woods      = {'name'    : 'woods',
                  'maptypes': [mapa.MAPTYPES.wood]}

    from_file  = {'name'    : 'from_file',
                  'maptypes': [mapa.MAPTYPES.special]}

    # hogsmeade, london, ministery, diagon_alley, gringotts, country (riddles,burrow,etc)

class World:
    """
    Entire world of the game.

    Methods:
      __init__
      initWorld

    Variables:
      wrldseed  - seed for random number generator
      wrldrg    - global random number generator
      levels    - generated levels of the world
      players   - players of the game
    """
    def __init__(self):
        """
        Initialize game's world.
        """
        self.wrldseed = calendar.timegm(time.gmtime())
        log.debug("World seed: %s" % str(self.wrldseed))
        # self.wrldrg = tcod.random_new_from_seed(self.wrldseed)
        self.wrldrg = tcod.random_new()

        self.levels = {} # levels' empty graph

        self.players = []

        self.initWorld()

    def initWorld(self):
        """
        Initialize the  world's map graph.

        The world is composed of a series of levels (nodes) connected
        with each other (as edges in a graph). The first level (index
        0) is the entrance of the game (where it all begins).

        ref: http://www.python.org/doc/essays/graphs.html

        TODO:
          - Levels should be initilized in a non-hard-coded way, maybe
            reading the definition from some file. [CURRENTLY IT'S
            HARD-CODED!]
        """
        levels = [] # just a list of all the levels in the world

        levels.append(level.Level(0, 'init', WORLDBRANCHES.dungeons, self.wrldrg))
        levels.append(level.Level(1, '1st floor', WORLDBRANCHES.classrooms, self.wrldrg))
        levels.append(level.Level(-1, '1st dung', WORLDBRANCHES.dungeons, self.wrldrg))

        # graph relating levels to connecting levels
        self.levels[levels[0].name] = [levels[0], levels[1], levels[2]]
        self.levels[levels[1].name] = [levels[1], levels[0]]
        self.levels[levels[2].name] = [levels[2], levels[0]]

    def new_game(self):
        """
        Initialize for a new game.

        -Each existent player is placed on level 1.
         Placement should include positioning player's coordiantes in
         a valid room

        Returns:
          level.Level number 1
        """
        # create initial player
        self.players.append(player.Player('@', 'blue', 'Player', 0, 0))

        initlev = self.levels['init'][0]

        for p in self.players:
            initlev.objects.append(p)
            initlev.players.append(p)
            p.curlevel = initlev
            p.x,p.y = p.curlevel.mapa.get_stairs(st='start')

        return initlev
