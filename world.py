"""
world.py

RogueWarts world.

The World holds all the game information which is not related to the
UI or to the way the game evolves through time (which belongs to the
engine). Ie, it holds all the game data and its current state.

  class World         : the world model class

  class WORLDBRANCHES : the branches on which the levels are grouped
"""

import libtcod.libtcodpy as tcod
import level, mapa
import player
import logging
import time, calendar

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
                  'maptypes': [mapa.MAPTYPES.classrooms, mapa.MAPTYPES.classrooms_2]}

    dungeons   = {'name'    : 'dungeons',
                  'maptypes': [mapa.MAPTYPES.dungeon, mapa.MAPTYPES.dungeon_2]}

    woods      = {'name'    : 'woods',
                  'maptypes': [mapa.MAPTYPES.wood]}

    # hogsmeade, london, ministery, diagon_alley, gringotts, country (riddles,burrow,etc)

class World:
    """
    Entire world of the game.

    Methods:
      __init__
      initWorld

    Variables:
      wrldseed  - seed for random number generator
      wrldrg    - random number generator
      levels    - generated levels of the world
      players   - players of the game
    """
    def __init__(self):
        """
        Initialize game's world.
        """
        self.wrldseed = calendar.timegm(time.gmtime())
        log.debug("World seed: %s" % str(self.wrldseed))
        self.wrldrg = tcod.random_new_from_seed(self.wrldseed)

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

        Levels should be initilized in a non-hard-coded way, maybe
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

        for p in self.players:
            p.curlevel = self.levels['init'][0]
            # position p.x,p.y in a valid room

        return self.levels['init'][0]
