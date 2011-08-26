'''
level.py
'''

import libtcod.libtcodpy as tcod
import logging
import time, calendar
import map
import util

log = logging.getLogger('roguewarts.level')

MAX_ROOM_MONSTERS = 3
MAX_ROOM_ITEMS = 2

class WORLDBRANCHES:
    """Branches of the world"""
    classrooms = {'name': 'classrooms',
                  'maptypes': [map.MAPTYPES.classrooms, map.MAPTYPES.classrooms_2]}
    dungeons   = {'name': 'dungeons',
                  'maptypes': [map.MAPTYPES.dungeon, map.MAPTYPES.dungeon_2]}
    woods      = {'name': 'woods',
                  'maptypes': [map.MAPTYPES.wood]}
    hogsmeade  = None
    # london, ministery, diagon_alley, gringotts, country (riddles,burrow,etc)

class Level:
    """A level in the world class"""
    def __init__(self, numlevel, name, branch, rng):
        self.objects = []
        self.numlevel = numlevel
        self.name = name
        self.ismaraudable = False

        if branch['name'] == 'classrooms':
            maptype = numlevel < 5 and branch['maptypes'][0] or branch['maptypes'][1]
        elif branch['name'] == 'dungeons':
            maptype = numlevel > -5 and branch['maptypes'][0] or branch['maptypres'][1]
        elif branch['name'] == 'woods':
            maptype = branch['maptypes'][0]
        if numlevel > 10 or numlevel < -10:
            maptype = map.MAPTYPES.labyrinth

        if util.debug or True:
            maptype=map.MAPTYPES.dungeon_2 # debugging dungeons
        self.map = map.Map(maptype, rng)

    def place_objects(self):
        """Place random objects in level"""
        pass
