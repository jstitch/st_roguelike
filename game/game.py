"""
game.py

RogueWarts game control logic.

I intend RogeWarts to be programmed in a fashion following certain
architecture, like the ones seen in webapps (MVC).

Even if roguewarts.py holds the main routine and loop, game.py is
intented to be the Control layer.

Following the analogy, ui.py would be the View layer (supported by
some specific ui wrapper), but including the input handling logic too.

And the rest of the classes (level.py, map.py, ai.py, etc.) would be
the Model layer.

This module holds the following structures:

  map STATES         : lists the possible state a game is in. Is the user
                       playing the game? is he/she configuring it? is
                       the game paused? has the game finished and the
                       user asked to exit?

  map MESSAGETYPES   : lists the possible messages the game can give
                       to the user and a color which is used to draw
                       that type of message

  class Game         : Control class for RogueWarts: game initialization
                       (including UI and loading/saving to disk),
                       transition between game states, initializing
                       the Model

  class GameUtil     : Engine utilities (print user messages,)

  class Gameplay     : Manager class, methods to loop the game on the
                       PLAYING state.  Responds to user input, calls
                       View routines, updates / uses the Model
                       routines
"""

import logging
import libtcod.libtcodpy as tcod
import traceback as tbck

from util import _
import util
import ui.ui as ui
import world.world as world

log = logging.getLogger('roguewarts.game')

"""Game states."""
STATES = {'PLAYING'  : 0,
          'EXIT'     : -1,
          'PAUSE'    : 1,
          'CONFIG'   : 2,
          'MAINMENU' : 3}

"""User messages types and colors."""
MESSAGETYPES = {'NORMAL'  : 'grey',
                'SUCCESS' : 'green',
                'WARNING' : 'yellow',
                'ALERT'   : 'red'}

class Game:
    """
    Game control class.

    Methods:
      __init__
      terminate
      iterate
      new_game
      main_menu
      exit

    Variables:
      state  - current game state
      world  - game world
      curp   - current player
      curl   - current level
      util   - engine utilities instance
      ui     - game ui instance
      update - engine update cycle instance
    """
    def __init__(self, uilib, uiparams):
        """
        Initialize game engine, UI included.

        Arguments:
          uilib    : name of the UI lib to use
          uiparams : params for the UI lib (see ui.py doc for more
                     info)
        """
        self.state = STATES['MAINMENU']

        self.world = world.World()
        self.curp = None
        self.curl = None

        self.util = GameUtil(self)
        self.ui = ui.UI(uilib, uiparams)
        self.update = Gameplay(self, self.util, self.ui) # default update cycle: gameplay

        try:
            self.main_menu()
        except Exception as e:
            log.error(tbck.format_exc())
            self.ui.close()
            raise util.RoguewartsException("initerror: " + str(e))

    def terminate(self):
        """
        Terminate game engine.

        -Closes the UI cleanly
        """
        self.ui.close()

    def iterate(self):
        """
        Iterate on the current state.

        Depends on the manager class to have a play method.
        """
        self.update.play()

    def main_menu(self):
        """
        Go to main menu state.
        """
        self.state = STATES['MAINMENU']

        self.new_game() # test call, should be main_menu routines

    def new_game(self):
        """
        Go to new game state.

        -Initializes world for a new game.
        -Retrieves current level #1
        -Adds welcome message
        """
        self.state = STATES['PLAYING']

        self.curl = self.world.new_game()
        self.curp = self.world.players[0]

        self.util.add_message(_("Welcome to RogueWarts anonymous!"), MESSAGETYPES['SUCCESS'])
        if util.debug:
            self.util.add_message("x:%d,y:%d" % (self.curp.x, self.curp.y), MESSAGETYPES['ALERT'])

        self.ui.refresh_map(self.curl, self.curp.x, self.curp.y)

    def exit(self):
        """
        Go to exit game state.
        """
        self.state = STATES['EXIT']

class GameUtil:
    """
    Game engine utilities.

    Methods:
      __init__
      add_message

    Variables:
      qmessage - messages queue
      engine   - ref to the engine
    """
    def __init__(self, engine):
        """
        Initialize class variables.

        Arguments:
          engine : a reference to the Game engine class
        """
        self.engine = engine

        self.qmessage = []

    def add_message(self, message, mtype=MESSAGETYPES['NORMAL']):
        """
        Enqueue and display a message.

        Arguments:
          message : message string to display
          mtype   : MESSAGETYPES to define message properties
                    (color,). Default: NORMAL
        """
        self.qmessage.append(util.Message(message, {'color':mtype}))
        self.engine.ui.refresh_message(queue=self.qmessage)

class Gameplay:
    """
    Gameplay manager class, manage game during PLAYING state.

    Methods:
      __init__
      play
      action

    Variables:
      action_type - what action has been taken
      engine      - ref to game engine
      util        - ref to engine utils
      ui          - ref to ui
    """

    """Action types."""
    ACTIONS = {'took-turn'       : 0,
               'exit-game'       : 1,
               'didnt-take-turn' : 2}

    def __init__(self, engine, engutil, engui):
        """
        Initialize class variables.

        Arguments:
          engine : a reference to the Game engine class
          util   : a reference to the Engine Utilities class
          ui     : a reference to the UI
        """
        self.engine = engine
        self.util = engutil
        self.ui = engui

        self.action_type = None

    def play(self):
        """
        Manage iteration of standard gameplay update cycle.

        Manages user input / screen output for a game, rendering map,
        objects and monsters, and allowing user to make an input in a
        non-blocking manner, also runs the AI for the monsters to take
        a turn
        """
        try:
            if self.ui.is_closed():
                self.engine.exit()

            # For each player
            for p in self.engine.world.players:

                self.engine.curp = p
                self.engine.curl = p.curlevel

                # refresh display
                if self.action_type == self.ACTIONS['took-turn']:
                    if util.debug:
                        self.util.add_message("x:%d,y:%d" % (self.engine.curp.x, self.engine.curp.y), MESSAGETYPES['ALERT'])
                    self.ui.refresh_map(self.engine.curl, self.engine.curp.x, self.engine.curp.y)

                # clear objects in current level display
                for obj in self.engine.curl.objects:
                    obj.clear()
                    self.ui.clear_obj(obj)

                # execute action taken
                self.action_type = self.action(self.ui.handle_input())
                if self.action_type == self.ACTIONS['exit-game']:
                    self.engine.exit()
                    return

            # let monsters take turn, only if it applies (for speed/last input command considerations)
            if self.engine.state == STATES['PLAYING'] and self.action_type != self.ACTIONS['didnt-take-turn']:
                for obj in self.engine.curl.objects:
                    if obj.ai:
                        obj.ai.take_turn()
        except util.RoguewartsException as e:
            try:
                log.error(tbck.format_exc())
                self.util.add_message(str(e), MESSAGETYPES['ALERT'])
                self.action_type = ''
            except Exception as e2:
                log.critical(str(e) + " -> " + str(e2))
                raise Exception("ERROR: could not raise roguewarts exception!")

    def action(self, player_action):
        """
        Execute some action.

        Arguments:
          player_action : action to execute

        Returns:
          string with result of action taken for the play method to
          interpret, from ACTIONS map

        TODO:
          - refactor to add actions coming from a
            objects.player.Player class . Actions should come frome
            the current update class but also from the specific type
            of player. For example, movement actions should go in
            certain type of Player, while 'quit' command is part of
            the update class
        """
        # quit game
        if player_action == 'q' or player_action == tcod.KEY_ESCAPE:
            return self.ACTIONS['exit-game']

        # move player
        # UP
        if player_action == tcod.KEY_UP or player_action == tcod.KEY_KP8:
            if self.engine.curp.y > 0:
                self.engine.curp.move(0,-1)
                return self.ACTIONS['took-turn']
        # DOWN
        elif player_action == tcod.KEY_DOWN or player_action == tcod.KEY_KP2:
            if self.engine.curp.y < self.engine.curl.mapa.h - 1:
                self.engine.curp.move(0,1)
                return self.ACTIONS['took-turn']
        # LEFT
        elif player_action == tcod.KEY_LEFT or player_action == tcod.KEY_KP4:
            if self.engine.curp.x > 0:
                self.engine.curp.move(-1,0)
                return self.ACTIONS['took-turn']
        # RIGHT
        elif player_action == tcod.KEY_RIGHT or player_action == tcod.KEY_KP6:
            if self.engine.curp.x < self.engine.curl.mapa.w - 1:
                self.engine.curp.move(1,0)
                return self.ACTIONS['took-turn']
        # LEFT-UP
        elif player_action == tcod.KEY_KP7:
            if self.engine.curp.x > 0 and self.engine.curp.y > 0:
                self.engine.curp.move(-1,-1)
                return self.ACTIONS['took-turn']
        # RIGHT-UP
        elif player_action == tcod.KEY_KP9:
            if self.engine.curp.x < self.engine.curl.mapa.w - 1 and self.engine.curp.y > 0:
                self.engine.curp.move(1,-1)
                return self.ACTIONS['took-turn']
        # LEFT-DOWN
        elif player_action == tcod.KEY_KP1:
            if self.engine.curp.x > 0 and self.engine.curp.y < self.engine.curl.mapa.h - 1:
                self.engine.curp.move(-1,1)
                return self.ACTIONS['took-turn']
        # RIGHT-DOWN
        elif player_action == tcod.KEY_KP3:
            if self.engine.curp.x < self.engine.curl.mapa.w - 1 and self.engine.curp.y < self.engine.curl.mapa.h - 1:
                self.engine.curp.move(1,1)
                return self.ACTIONS['took-turn']

        return self.ACTIONS['didnt-take-turn']
