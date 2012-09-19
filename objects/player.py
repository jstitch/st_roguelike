"""
player.py

RogueWarts class for a user controlled character.

The Player should be a Fighter object.

  class Player : the Player definition
"""

import logging

import libtcod.libtcodpy as tcod
import game.game

import objeto

log = logging.getLogger('roguewarts.player')

class Player(objeto.Object):
    """
    Player class.

    A player may be controlled by the user. Any other character not
    controlled by the user, is named a 'monster' and has an AI
    associated with it.

    Methods:
      __init__

    Variables:

    TODO:
      - Also, the fighter component should be init at the Objeto
        class, not here. Perhaps Player class should be another type
        of component too?
    """
    def __init__(self, char, color, name, x, y):
        """
        Initilize player.

        Defines the fighter component of the player (giving it
        hitpoints, power, etc.)
        """
        fighter_component = objeto.Fighter() # hp=30, defense=2,
                                             # power=5,
                                             # death_function=player_death
        objeto.Object.__init__(self, char, color, name, x, y, True, fighter_component)

    def action(self, player_action):
        """
        Execute player action.

        Arguments:
          player_action : action to execute

        Returns:
          string with result of action taken for the enginte to
          interpret
        """
        # Move player
        # UP
        if player_action == tcod.KEY_UP or player_action == tcod.KEY_KP8:
            if self.y > 0:
                self.move(0,-1)
                return game.game.Gameplay.ACTIONS['took-turn']
        # DOWN
        elif player_action == tcod.KEY_DOWN or player_action == tcod.KEY_KP2:
            if self.y < self.curlevel.mapa.h - 1:
                self.move(0,1)
                return game.game.Gameplay.ACTIONS['took-turn']
        # LEFT
        elif player_action == tcod.KEY_LEFT or player_action == tcod.KEY_KP4:
            if self.x > 0:
                self.move(-1,0)
                return game.game.Gameplay.ACTIONS['took-turn']
        # RIGHT
        elif player_action == tcod.KEY_RIGHT or player_action == tcod.KEY_KP6:
            if self.x < self.curlevel.mapa.w - 1:
                self.move(1,0)
                return game.game.Gameplay.ACTIONS['took-turn']
        # LEFT-UP
        elif player_action == tcod.KEY_KP7:
            if self.x > 0 and self.y > 0:
                self.move(-1,-1)
                return game.game.Gameplay.ACTIONS['took-turn']
        # RIGHT-UP
        elif player_action == tcod.KEY_KP9:
            if self.x < self.curlevel.mapa.w - 1 and self.y > 0:
                self.move(1,-1)
                return game.game.Gameplay.ACTIONS['took-turn']
        # LEFT-DOWN
        elif player_action == tcod.KEY_KP1:
            if self.x > 0 and self.y < self.curlevel.mapa.h - 1:
                self.move(-1,1)
                return game.game.Gameplay.ACTIONS['took-turn']
        # RIGHT-DOWN
        elif player_action == tcod.KEY_KP3:
            if self.x < self.curlevel.mapa.w - 1 and self.y < self.curlevel.mapa.h - 1:
                self.move(1,1)
                return game.game.Gameplay.ACTIONS['took-turn']

        return game.game.Gameplay.ACTIONS['didnt-take-turn']
