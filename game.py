'''
game.py
'''

import logging
import libtcod.libtcodpy as tcod
import ui, world
from util import _
import util

log = logging.getLogger('roguewarts.game')

class STATES:
    """Game states"""
    PLAYING = 0
    EXIT = -1
    PAUSE = 1
    CONFIG = 2

class MESSAGETYPES:
    """User messages types"""
    NORMAL  = 'grey'
    SUCCESS = 'green'
    WARNING = 'yellow'
    ALERT   = 'red'

class Game:
    """Game control class"""
    def __init__(self, uilib, maximize, forcedim):
        self.state = STATES.CONFIG
        self.world = world.World()
        self.update = self.gameplay
        self.ui = None
        self.qmessage = []
        # at last, init UI
        self.ui = ui.UI(uilib, maximize, forcedim)

        self.action_type = None

        self.dumx = 0
        self.dumy = 0

    def new_game(self):
        """Initialize for a new game"""
        self.world.new_game()
        self.add_message(message=_("Welcome to RogueWarts anonymous!"), type=MESSAGETYPES.SUCCESS)
        if util.debug:
            self.add_message("x:%d,y:%d" % (self.dumx, self.dumy), MESSAGETYPES.ALERT)
        self.ui.refresh_map(self.world, self.dumx, self.dumy)

    def terminate(self):
        """Terminates game"""
        self.ui.close()

    def add_message(self, message, type=MESSAGETYPES.NORMAL):
        """Enqueue a message"""
        self.qmessage.append(util.Message(message, {'color':type}))
        self.ui.refresh_message(queue=self.qmessage)

    def gameplay(self):
        """Standard gameplay update cycle"""
        try:
            if self.ui.is_closed():
                self.exit()

            # refresh display
            if self.action_type == 'took-turn':
                if util.debug:
                    self.add_message("x:%d,y:%d" % (self.dumx, self.dumy), MESSAGETYPES.ALERT)
                self.ui.refresh_map(self.world, self.dumx, self.dumy)

            # clear objects in current level display
            for obj in self.world.cur_level.objects:
                obj.clear()
                self.ui.clear_obj(obj)

            # execute action taken
            self.action_type = self.action(self.ui.handle_input())
            if self.action_type == 'exit':
                self.exit()
                return

            # let monsters take turn, only if it applies (for speed/last input command considerations)
            if self.state == STATES.PLAYING and self.action_type != 'didnt-take-turn':
                for obj in self.world.cur_level.objects:
                    if object.ai:
                        obj.ai.take_turn()
        except util.RoguewartsException as e:
            try:
                log.error(str(e))
                self.add_message(str(e), MESSAGETYPES.ALERT)
                self.action_type = ''
            except Exception as e2:
                log.critical(str(e) + " -> " + str(e2))
                raise Exception("ERROR: could not raise roguewarts exception!")

    def action(self, player_action):
        """Execute some action"""
        if player_action == 'q' or player_action == tcod.KEY_ESCAPE:
            return 'exit'

        if player_action == tcod.KEY_UP:
            if self.dumy > 0:
                self.dumy -= 1
                return 'took-turn'
        elif player_action == tcod.KEY_DOWN:
            if self.dumy < self.world.cur_level.map.h - 1:
                self.dumy += 1
                return 'took-turn'
        elif player_action == tcod.KEY_LEFT:
            if self.dumx > 0:
                self.dumx -= 1
                return 'took-turn'
        elif player_action == tcod.KEY_RIGHT:
            if self.dumx < self.world.cur_level.map.w - 1:
                self.dumx += 1 
                return 'took-turn'

        return 'didnt-take-turn'

    def exit(self):
        """Exit game"""
        self.state = STATES.EXIT
