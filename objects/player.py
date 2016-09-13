"""
player.py

RogueLike class for a user controlled character.

The Player should be a Fighter object.

  class Player : the Player definition
"""

import logging
import libtcod.libtcodpy as tcod

from world import mapa
from world.tile import TILETYPES
import objeto

log = logging.getLogger('roguelike.player')

class Player(objeto.Object):
    """
    Player class.

    A player may be controlled by the user. Any other character not
    controlled by the user, is named a 'monster' and has an AI
    associated with it.

    Methods:
      __init__

    Variables:
      fov_map : a player has a field of view

    TODO:
      - refactor to add actions specific to the player here. Also, the
        fighter component should be init at the Objeto class, not
        here. Perhaps Player class should be another type of component
        too?
    """
    def __init__(self, char, color, name, x, y, curlevel):
        """
        Initilize player.

        Defines the fighter component of the player (giving it
        hitpoints, power, etc.)
        """
        fighter_component = objeto.Fighter() # hp=30, defense=2,
                                             # power=5,
                                             # death_function=player_death
        objeto.Object.__init__(self, char, color, name, x, y, curlevel, True, fighter_component)

        self.ini_fov_map()
        self.compute_fov_map()

    def move(self, dx, dy):
        """
        Moves player.

        Moves the player coordinates by dx and dy.
        After moving, FOV map is recomputed
        """
        super(Player,self).move(dx, dy)
        self.compute_fov_map()

    def ini_fov_map(self):
        """
        Inits the FOV map for player's current level.
        """
        self.fov_map = tcod.map_new(self.curlevel[0].mapa.w, self.curlevel[0].mapa.h)
        for y in range(self.curlevel[0].mapa.h):
            for x in range(self.curlevel[0].mapa.w):
                tcod.map_set_properties(self.fov_map, x, y, not TILETYPES[self.curlevel[0].mapa.mapa[x][y].tipo]['block_sight'], not TILETYPES[self.curlevel[0].mapa.mapa[x][y].tipo]['block_pass'])

    def compute_fov_map(self):
        """Recompute FOV map for player."""
        tcod.map_compute_fov(self.fov_map, self.x, self.y, radius=15, light_walls=True, algo=tcod.FOV_BASIC)
