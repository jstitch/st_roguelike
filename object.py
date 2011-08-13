'''
object.py
'''

import logging
import math

log = logging.getLogger('roguewarts.object')

class Object:
    """Object class"""
    def __init__(self, x = -1, y = -1, char, color, name, blocks = False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        """Move object to (x+dx, y+dy)"""
        self.x = self.x + dx
        self.y = self.y + dy

    def distance(self, x, y):
        """Distance to some coordinates"""
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def clear(self):
        """Clear object"""
        pass
