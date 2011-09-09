"""
player.py

RogueWarts class for a user controlled character.

The Player should be a Fighter object.

  class Player : the Player definition
"""

import logging
import object

log = logging.getLogger('roguewarts.player')

class Player(object.Object):
    """
    Player class.

    A player may be controlled by the user. Any other character not
    controlled by the user, is named a 'monster' and has an AI
    associated with it.

    Methods:
      __init__

    Variables:
      curlevel - level at which this player is currently hacking
                 around
    """
    def __init__(self, char, color, name, x, y):
        """
        Initilize player.

        Defines the fighter component of the player (giving it
        hitpoints, power, etc.)
        """
        fighter_component = object.Fighter() # hp=30, defense=2,
                                             # power=5,
                                             # death_function=player_death
        object.Object.__init__(self, char, color, name, x, y, True, fighter_component)
        self.curlevel = None