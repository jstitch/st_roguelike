'''
ui.py
'''

import logging
import sys, game
import util

log = logging.getLogger('roguewarts.ui')

# minimum size of the window
SCREEN_WIDTH = 105
SCREEN_HEIGHT = 36

class UI:
    """UI class"""
    def __init__(self, uilib, maximize, forcedim):
        # Uses ducktyping to load the correct UI library. Needs a
        # uiwrappers.library_wrapper lib with uilib_wrapper class implementing
        # all same methods as libtcod_wrapper and curses_wrapper do (even
        # though, libtcod is used also for other things in the game,
        # independently of the UI thing). This gives the possibility to use
        # any other UI library, like for example GTK or whatever, using
        # libtcod in the background for the wonderfully implemented roguelike
        # features of this library (also, curses & libtcod uses number of
        # chars for coordinates/dimensions, while others may use pixels or
        # anything elso, so a translation from chars to whatever should be
        # necessary...)
        try:
            __import__("uiwrappers." + uilib + "_wrapper")
            self.ui = getattr(sys.modules["uiwrappers." + uilib + "_wrapper"], uilib + "_wrapper")()
            log.info("Successfully imported " + uilib + " library")
        except ImportError:
            log.critical("Can't import wrapper library for " + uilib)
            raise ImportError("ERROR: can't import library " + "uiwrappers." + uilib + "_wrapper")
        except AttributeError:
            log.critical("Can't instantiate ui class " + uilib + "_wrapper")
            raise AttributeError("ERROR: can't instantiate ui class " + uilib + "_wrapper" + " in library" + uilib)
        except Exception as e:
            log.critical("Can't initialize ui: %s" % str(e))
            raise Exception("ERROR: can't initialize ui")

        # finally, initialize UI screen
        try:
            self.maxx, self.maxy = self.ui.init(SCREEN_WIDTH, SCREEN_HEIGHT, maximize, forcedim)
        except AttributeError as e:
            self.ui.close()
            log.critical(str(e))
            raise AttributeError("ERROR: could not initialize UI")
        except Exception as e:
            self.ui.close()
            log.critical("Error while initializing UI: %s" % str(e))
            raise Exception("ERROR: while initializing UI")

        # validates screen size
        if (self.maxx, self.maxy) < (0, 0):
            self.ui.close()
            log.critical("Screen needs to be at least (%d, %d). Current size is (%d, %d)" %
                         (SCREEN_WIDTH, SCREEN_HEIGHT, self.maxx * -1, self.maxy * -1))
            raise Exception("ERROR: screen size is too low, you need at least (%d, %d)" % (SCREEN_WIDTH, SCREEN_HEIGHT))

        if util.debug:
            try:
                self.ui.test()
            except Exception as e:
                self.ui.close()
                log.critical("Error testing screen: %s" % str(e))
                raise Exception("ERROR: at screen test")
        log.debug("Window dimensions: (%s, %s)" % (str(self.maxx), str(self.maxy)))
        log.debug("Main console: %s" % str(self.ui.main))
        log.debug("Message console: %s" % str(self.ui.messages))
        log.debug("Player stats console: %s" % str(self.ui.playerstats))
        log.debug("Game stats console: %s" % str(self.ui.gamestats))
        log.debug("Inventory console: %s" % str(self.ui.inventory))

    def close(self):
        """Closes UI"""
        try:
            self.ui.close()
        except AttributeError as e:
            log.critical(str(e))
            raise AttributeError("ERROR: could not close UI")

    def is_closed(self):
        """Detects if UI has been closed by the user"""
        try :
            return self.ui.is_closed()
        except AttributeError as e:
            log.critical(str(e))
            raise AttributeError("ERROR: could not detect if UI is closed")

    def handle_input(self):
        """Handle user input"""
        try:
            return self.ui.getkey()
        except AttributeError as e:
            log.critical(str(e))
            raise AttributeError("ERROR: could not get key from UI")

    def refresh_message(self, queue=[]):
        """Refresh messages area"""
        try:
            self.queue = queue # backup queue
            self.ui.message(queue)
            self.flush('messages')
        except AttributeError as e:
            log.critical(str(e))
            raise AttributeError("ERROR: could not print messages")

    def refresh_map(self, world, x, y):
        """Render current level"""
        try:
            if x < 0 or y < 0 or x > world.cur_level.map.w - 1 or y > world.cur_level.map.h - 1:
                raise util.RoguewartsException("ERROR: char out of map bounds! (x=%d,y=%d) when max map is (%d,%d)" %
                                               (x,y,world.cur_level.map.w - 1,world.cur_level.map.h - 1))

            # to render correctly, we need the character dimensions of the
            # area where the map is to be drawn
            try:
                conarea_w, conarea_h = self.ui.getareadims()
            except Exception as e:
                log.critical(str(e))
                raise Exception("ERROR: could not determine draw area dimensions")

            level = world.cur_level
            
            # fov calculations... (shouldn't be here, should already be calculated elsewhere...)

            # determine map coordinates to begin rendering according to map size
            # fitting in console size and (x,y) which are given to try and center
            # the map in the console. If it's not possible to center, render the
            # map and put (x,y) in an offset to a side of the map
            (minx, miny) = (level.map.w > conarea_w and # if map is smaller than console...
                            (x - conarea_w//2 > 0 and # if not, if coordinate is beyond left half of console...
                             (x + conarea_w//2 < level.map.w and # see if it's beyond right half of console...
                              x - conarea_w//2 or # if it is, draw map from x - half console
                              level.map.w - conarea_w) # if it is not beyond right half (but it is beyond left half), draw from map width-half console
                             or 0) # if it's not beyond left half, map will be rendered from the beginning left
                            or 0, # if map was smaller than console, it will be rendered all
                            level.map.h > conarea_h and
                            (y - conarea_h//2 > 0 and # the same applies for y coord and map height
                            (y + conarea_h//2 < level.map.h and
                             y - conarea_h//2 or
                             level.map.h - conarea_h)
                            or 0) or 0)
            (maxx, maxy) = (level.map.w if level.map.w <= conarea_w else conarea_w + minx,
                            level.map.h if level.map.h <= conarea_h else conarea_h + miny)

            # draw objects in map...

            # sent to ui lib
            self.ui.render(level, x, y, minx, miny, maxx, maxy)

        except AttributeError as e:
            log.critical(str(e))
            raise AttributeError("ERROR: could not render level")

        self.flush('map')

    def flush(self, area='all'):
        """Flush screen"""
        try:
            self.ui.flush(area)
        except AttributeError as e:
            log.critical(str(e))
            raise AttributeError("ERROR: could not flush UI screen")

    def clear_obj(self, object):
        """Clear some object in display"""
        pass
