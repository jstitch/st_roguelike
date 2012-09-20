"""
player.py

RogueWarts class for a user controlled character.

The Player should be a Fighter.

  class Player : the Player definition
"""

import logging

import libtcod.libtcodpy as tcod
import game.game

import objeto

log = logging.getLogger('roguewarts.player')

class Player:
    """
    Player class.

    A player may be controlled by the user. Any other character not
    controlled by the user, is named a 'monster' and has an AI
    associated with it.

    Methods:
      __init__

    Variables:
      fighter - the fighter component which gives hp, defense, power,
                etc. to the player
    """
    def __init__(self):
        """
        Initilize object.

        Defines the fighter component of the player (giving it
        hitpoints, power, etc.)
        """
        self.fighter = objeto.Fighter() # hp=30, defense=2,
                                        # power=5,
                                        # death_function=player_death

    def init(self):
        """
        Initialize player.

        These initializations are done here since every player must
        have them. This way freeing the Object owner of the
        responsibility of defining things that are proper of a player,
        not necessarily of any Object object.

        - Defines fighter component on objeto owner.
        - Defines blocks property to True
        """
        self.owner.fighter = self.fighter
        self.owner.blocks = True

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
            if self.owner.y > 0:
                self.owner.move(0,-1)
                return game.game.Gameplay.ACTIONS['took-turn']
        # DOWN
        elif player_action == tcod.KEY_DOWN or player_action == tcod.KEY_KP2:
            if self.owner.y < self.owner.curlevel.mapa.h - 1:
                self.owner.move(0,1)
                return game.game.Gameplay.ACTIONS['took-turn']
        # LEFT
        elif player_action == tcod.KEY_LEFT or player_action == tcod.KEY_KP4:
            if self.owner.x > 0:
                self.owner.move(-1,0)
                return game.game.Gameplay.ACTIONS['took-turn']
        # RIGHT
        elif player_action == tcod.KEY_RIGHT or player_action == tcod.KEY_KP6:
            if self.owner.x < self.owner.curlevel.mapa.w - 1:
                self.owner.move(1,0)
                return game.game.Gameplay.ACTIONS['took-turn']
        # LEFT-UP
        elif player_action == tcod.KEY_KP7:
            if self.owner.x > 0 and self.owner.y > 0:
                self.owner.move(-1,-1)
                return game.game.Gameplay.ACTIONS['took-turn']
        # RIGHT-UP
        elif player_action == tcod.KEY_KP9:
            if self.owner.x < self.owner.curlevel.mapa.w - 1 and self.owner.y > 0:
                self.owner.move(1,-1)
                return game.game.Gameplay.ACTIONS['took-turn']
        # LEFT-DOWN
        elif player_action == tcod.KEY_KP1:
            if self.owner.x > 0 and self.owner.y < self.owner.curlevel.mapa.h - 1:
                self.owner.move(-1,1)
                return game.game.Gameplay.ACTIONS['took-turn']
        # RIGHT-DOWN
        elif player_action == tcod.KEY_KP3:
            if self.owner.x < self.owner.curlevel.mapa.w - 1 and self.owner.y < self.owner.curlevel.mapa.h - 1:
                self.owner.move(1,1)
                return game.game.Gameplay.ACTIONS['took-turn']

        return game.game.Gameplay.ACTIONS['didnt-take-turn']
