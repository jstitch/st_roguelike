'''
world.py
'''

import libtcod.libtcodpy as tcod
import level
import logging
import time, calendar

log = logging.getLogger('roguewarts.level')

class World:
    """Entire world of the game"""
    def __init__(self):
        self.wrldseed = calendar.timegm(time.gmtime())
        log.debug("World seed: %s" % str(self.wrldseed))
        self.wrldrg = tcod.random_new_from_seed(self.wrldseed)
        self.levels = {} # levels graph (nodes = levels / edges = connections between levels)
        self.cur_level = None
        self.initWorld()

    def initWorld(self):
        """Init World"""
        levels = [] # just a list of all the levels in the world
        levels.append(level.Level(0, 'init', level.WORLDBRANCHES.dungeons, self.wrldrg))
        # levels.append(level.Level(1, '1st floor', level.WORLDBRANCHES.classrooms, self.wrldrg))
        # levels.append(level.Level(-1, '1st dung', level.WORLDBRANCHES.dungeons, self.wrldrg))

        # graph relating levels to connecting levels
        self.levels[levels[0].name] = [levels[0]] # , levels[1], levels[2]]
        # self.levels[levels[1].name] = [levels[1], levels[0]]
        # self.levels[levels[2].name] = [levels[2], levels[0]]

    def new_game(self):
        """Initialize for a new game"""
        self.cur_level = self.levels['init'][0]
