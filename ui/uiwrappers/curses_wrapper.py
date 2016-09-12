"""
curses_wrapper.py

NCurses graphical UI library wrapper for RogueWarts.

For RogueWarts UI purposes, a class is a UI wrapper if it implements
certain methods. Look for the class documentation to see what methods
they are.

NOTE: In theory, using curses as UI library, may allow to run the game
in remote SSH/telnet sessions. BUT libtcod (which is also used for
other game-logic/non-graphic thigs), requires the game to be run
locally. At the roguecentral forums, I've been searching for a
possible solution to this. Right now libtcod won't allow remote
running, but recompiling it with certain changes in the libtcod
sourcode may allow this (note that this would only be necessary in the
'server' on which the game would run). I included a patch for libtcod
1.5.0 to achieve this.

  class curses_wrapper : implementation for RogueWarts UI using
                         NCurses
"""

import curses
import textwrap
import libtcod.libtcodpy as libtcod
import logging

import game.util as util

log = logging.getLogger('roguewarts.curses_wrapper')

class curses_wrapper:
    """
    Implementation for using ncurses as UI library.

    Methods:
      __init__
      init
      getareadims
      close
      is_closed
      getkey
      flush
      message
      render
      test
      test_area

    Variables:
      KEY_MAP      - key mapping between ncurses keys and libtcod
      COLORS       - color mapping between ncurses colors and libtcod
      scr          - ncurses WindowObject representing the whole screen
      (maxx, maxy) - whole screen dimensions
    """

    """Key mapping between ncurses keys and libtcod ones. I give
    preference for libtocd codes, so a mapping is
    necessary. http://docs.python.org/library/curses.html#constants"""
    KEY_MAP = {
        curses.KEY_LEFT  : libtcod.KEY_LEFT,
        curses.KEY_RIGHT : libtcod.KEY_RIGHT,
        curses.KEY_UP    : libtcod.KEY_UP,
        curses.KEY_DOWN  : libtcod.KEY_DOWN,
        ord('1')         : libtcod.KEY_KP1,
        ord('2')         : libtcod.KEY_KP2,
        ord('3')         : libtcod.KEY_KP3,
        ord('4')         : libtcod.KEY_KP4,
        ord('6')         : libtcod.KEY_KP6,
        ord('7')         : libtcod.KEY_KP7,
        ord('8')         : libtcod.KEY_KP8,
        ord('9')         : libtcod.KEY_KP9,
        27               : libtcod.KEY_ESCAPE
        }

    """Colors mapping between ncurses color combinations and libtcod
    common color names. Again, I give preference to libtcod here."""
    COLORS = {
        'black'     : {'n':  1, 'fg': curses.COLOR_BLACK,   'bg': curses.COLOR_BLACK},
        'red'       : {'n':  2, 'fg': curses.COLOR_RED,     'bg': curses.COLOR_BLACK},
        'green'     : {'n':  3, 'fg': curses.COLOR_GREEN,   'bg': curses.COLOR_BLACK},
        'yellow'    : {'n':  4, 'fg': curses.COLOR_YELLOW,  'bg': curses.COLOR_BLACK},
        'blue'      : {'n':  5, 'fg': curses.COLOR_BLUE,    'bg': curses.COLOR_BLACK},
        'magenta'   : {'n':  6, 'fg': curses.COLOR_MAGENTA, 'bg': curses.COLOR_BLACK},
        'cyan'      : {'n':  7, 'fg': curses.COLOR_CYAN,    'bg': curses.COLOR_BLACK},
        'white'     : {'n':  8, 'fg': curses.COLOR_WHITE,   'bg': curses.COLOR_BLACK},

        'orange'    : {'n':  9, 'fg': curses.COLOR_YELLOW,  'bg': curses.COLOR_RED},
        'chartreuse': {'n': 10, 'fg': curses.COLOR_GREEN,   'bg': curses.COLOR_BLUE},
        'sea'       : {'n': 11, 'fg': curses.COLOR_CYAN,    'bg': curses.COLOR_BLUE},
        'sky'       : {'n': 12, 'fg': curses.COLOR_YELLOW,  'bg': curses.COLOR_BLUE},
        'violet'    : {'n': 13, 'fg': curses.COLOR_MAGENTA, 'bg': curses.COLOR_BLUE},
        'pink'      : {'n': 14, 'fg': curses.COLOR_CYAN,    'bg': curses.COLOR_MAGENTA},

        'light_red'       : {'n': 15, 'fg': curses.COLOR_RED,     'bg': curses.COLOR_WHITE},
        'light_green'     : {'n': 16, 'fg': curses.COLOR_GREEN,   'bg': curses.COLOR_WHITE},
        'light_yellow'    : {'n': 17, 'fg': curses.COLOR_YELLOW,  'bg': curses.COLOR_WHITE},
        'light_blue'      : {'n': 18, 'fg': curses.COLOR_BLUE,    'bg': curses.COLOR_WHITE},
        'light_magenta'   : {'n': 19, 'fg': curses.COLOR_MAGENTA, 'bg': curses.COLOR_WHITE},
        'light_cyan'      : {'n': 20, 'fg': curses.COLOR_CYAN,    'bg': curses.COLOR_WHITE},

        'dark_red'       : {'n': 21, 'fg': curses.COLOR_RED,     'bg': curses.COLOR_BLACK},
        'dark_green'     : {'n': 22, 'fg': curses.COLOR_GREEN,   'bg': curses.COLOR_BLACK},
        'dark_yellow'    : {'n': 23, 'fg': curses.COLOR_YELLOW,  'bg': curses.COLOR_BLACK},
        'dark_blue'      : {'n': 24, 'fg': curses.COLOR_BLUE,    'bg': curses.COLOR_BLACK},
        'dark_magenta'   : {'n': 25, 'fg': curses.COLOR_MAGENTA, 'bg': curses.COLOR_BLACK},
        'dark_cyan'      : {'n': 26, 'fg': curses.COLOR_CYAN,    'bg': curses.COLOR_BLACK},

        'grey'        : {'n': 27, 'fg': curses.COLOR_WHITE, 'bg': curses.COLOR_BLACK},
        'dark_grey'   : {'n': 28, 'fg': curses.COLOR_BLACK, 'bg': curses.COLOR_BLACK},
        'light_grey'  : {'n': 29, 'fg': curses.COLOR_BLACK, 'bg': curses.COLOR_WHITE}
        }

    def __init__(self):
        """
        Initialize variables.
        """
        self.scr = None

    def init(self, (minwidth, minheight), areas, maximize=False, forcemindims=False):
        """
        Properly initialize UI wrapper.

        Initializes ncurses screen with:
         -noecho
         -cbreak
         -colors
         -cursor off
         -keypad on
         -nodelay on
         -inits appropriate color pairs

        Also determines screen size.

        Finally, initializes each game area as a ncurses subwindow.

        Arguments:

          (minwidth, minheight) : the minimum expected dimensions for
                                  the screen
          areas                 : areas dictionary (see package documentation for more
                                  info)
          maximize              : maximize screen dimensions. Default: False
          forcemindims          : forces screen dimensions to maximum allowed by the
                                  terminal. Default: False

        Returns:
          tuple with screen size in (x,y), negative numbers if
          terminal doesn't satisfies minimum requirements
        """
        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)
        self.scr.keypad(1)
        self.scr.nodelay(True)

        (self.maxy,self.maxx) = self.scr.getmaxyx()

        # if curses screen doesn't has required dimensions, returns negative
        # numbers as an indication to caller
        if self.maxy < minheight or self.maxx < minwidth:
            if not forcemindims:
                return (self.maxx * -1, self.maxy * -1)

        if not maximize and not forcemindims:
            self.maxx = minwidth
            self.maxy = minheight

        for color, v in curses_wrapper.COLORS.iteritems():
            curses.init_pair(v['n'], v['fg'], v['bg'])

        # consoles
        w = self.maxx
        h = self.maxy*10//100
        x = 0
        y = 0
        win = self.scr.subwin(h, w, y, x)
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': win, 'name': 'messages' }
        areas['messages'] = map_

        w = self.maxx*80//100 + (1 if self.maxx % 5 != 0 else 0)
        h = self.maxy*80//100 + (1 if self.maxy % 10 > 5 else 0)
        x = 0
        y = self.maxy*10//100
        win = self.scr.subpad(h, w, y, x)
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': win, 'name': 'main' }
        areas['main'] = map_

        w = self.maxx*20//100
        h = self.maxy*80//100 + (1 if self.maxy % 10 > 5 else 0)
        x = self.maxx*80//100 + (1 if self.maxx % 5 != 0 else 0)
        y = self.maxy*10//100
        win = self.scr.subwin(h, w, y, x)
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': win, 'name': 'playerstats' }
        areas['playerstats'] = map_

        w = self.maxx
        h = self.maxy*10//100
        x = 0
        y = self.maxy*90//100
        win = self.scr.subwin(h, w, y, x)
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': win, 'name': 'gamestats' }
        areas['gamestats'] = map_

        w = self.maxx//2
        h = 3*self.maxy//4
        x = self.maxx//4
        y = self.maxy//8
        win = self.scr.subwin(h, w, y, x)
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': win, 'name': 'inventory' }
        areas['inventory'] = map_

        return (self.maxx,self.maxy)

    def getareadims(self, area):
        """
        Get area dimensions.

        Arguments:
          area : the area which dimensions are required

        Returns:
          tuple with area dimensions (width, height)
        """
        return (area['w'], area['h'])

    def close(self):
        """
        Terminates UI.

        Closes ncurses.
        """
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def is_closed(self):
        """
        Tells if user closes window.

        NCurses has no 'windows' interface for the user to close via
        some button, external to the mechanisms of the game itself (as
        in other UIs, where maybe an X button or Alt-F4 key
        combination allows to close the program), so it always returns
        False.

        Return:
          boolean telling if UI has been closed by the user.
        """
        return False

    def getkey(self):
        """
        Get a key.

        Manages user input, using non-blocking methods.

        Returns:
          ASCII code for an alphanumeric key, else a mapped key (see
          KEY_MAP dictionary)
        """
        key = self.scr.getch()
        if key == curses.ERR:
            return None
        # map curses.special_key_codes to libtcod.key.vk_codes
        elif key in curses_wrapper.KEY_MAP:
            return curses_wrapper.KEY_MAP[key]
        elif key > 255:
            return repr(key)
        return chr(key)

    def flush(self, area):
        """
        Flush screen area.

        Arguments:
          area : the area to be flushed
        """
        area['con'].refresh()

    def message(self, queue, mess_area):
        """
        Displays a message queue in the message area.

        It takes only the last messages from the queue, depending on
        the screen area height. It also wraps up message texts when
        message length is too long.

        Arguments:
          queue     : game's messages queue
          mess_area : the screen area where messages are displayed
        """
        mess_area['con'].clear()

        qmess = []
        for i in range(mess_area['h']):
            try:
                qmess.append(queue[(i + 1) * -1])
            except IndexError:
                break

        qlines = []
        for mess in qmess:
            str_lines = textwrap.wrap(mess.message, mess_area['w'])
            qlines.extend([util.Message(line, mess.properties) for line in str_lines])

        for i in range(mess_area['h']):
            try:
                mess_area['con'].addstr(mess_area['h'] - i - 1,
                                        0,
                                        qlines[i].message,
                                        curses.color_pair(curses_wrapper.COLORS[qlines[i].properties['color']]['n']))
            except IndexError:
                break

        self.flush(mess_area)

    def render(self, level, x, y, minx, miny, maxx, maxy, main_area):
        """
        Renders current level.

        Takes the level map and draws each tile on it, according to
        its properties.

        Since the map may be bigger (or smaller) than the screen, it
        makes some calculations to center (or try it at best) on the
        given (x,y) coordinates.

        TODO:
          - draw level objects. It just draws the map (and the player
            but just in a testing manner)
          - instead of drawing from level.mapa, ui.py should call a
            draw routing in the wrapper, which should receive the
            contents to be drawn in a specific area, without any game
            details being revealed here. This would also remove the
            previous message() method

        Arguments:
          level       : the world.level with the map to render
          (x,y)       : the coordinates to be the center of the drawing
          (minx,miny) : the minimum coordinates from the map to be drawn
          (maxx,maxy) : the maximum coordinates from the map to be drawn
          main_area   : the area where the map is to be drawn
        """
        from world.tile import TILETYPES
        main_area['con'].clear()

        map_ = level.mapa

        # determine console coordinates to begin rendering according to map size
        (conx, cony) = ((main_area['w'] - map_.w)//2 if map_.w < main_area['w'] else 0,
                        (main_area['h'] - map_.h)//2 if map_.h < main_area['h'] else 0)

        # draw map tiles
        if util.debug:
            c = 0
        for my, cy in map(None, range(miny, maxy), range(cony, map_.h + cony)):
            for mx, cx in map(None, range(minx, maxx), range(conx, map_.w + conx)):
                visible = True # libtcod.map_is_in_fov(fov_map, x, y)
                try:
                    tile = map_.mapa[mx][my]
                # BUG: sometimes None appears on the map(?!)
                except Exception as e:
                    if util.debug:
                        c += 1
                    continue
                # it's out of the player's FOV, player will see it only if explored
                if not visible:
                    if tile.explored:
                        # draw map tile with char/color <- modifications for explored/not visible
                        pass
                # it's visible
                else:
                    # draw map tile with char/color <- as is since it is visible
                    try:
                        main_area['con'].addstr(cy, cx, TILETYPES[tile.tipo]['char'].encode('utf8'),
                                                curses.color_pair(curses_wrapper.COLORS[TILETYPES[tile.tipo]['color']]['n']))
                        main_area['con'].addstr(cony + y - miny, conx + x - minx, '@',
                                                curses.color_pair(curses_wrapper.COLORS['red']['n']))
                    except Exception as e:
                        pass
                    # since now it's visible, mark it as explored
                    tile.explored = True
        if util.debug:
            log.debug("none appeared %d times" % c)

        self.flush(main_area)

    def test(self, areas):
        """
        Test routine.

        Draws some test things in each area.

        Arguments:
          areas : the areas dictionary
        """
        self.scr.clear()

        # blit messages
        self.test_area(areas['messages'], 'red', '')

        # blit main
        self.test_area(areas['main'], 'yellow', '')

        # blit playerstats
        self.test_area(areas['playerstats'], 'green', '')

        # blit gamestats
        self.test_area(areas['gamestats'], 'blue', '')

        # blit inventory
        self.test_area(areas['inventory'], 'cyan', '')

        self.scr.addstr(self.maxy//2, self.maxx//2, curses.__name__)

    def test_area(self, area, fcolor, bcolor):
        """
        Draw routines to test game areas.

        Draws some test things in a specific area.

        Arguments:
          area   : area to be tested
          fcolor : foreground color to use for test
          bcolor : background color to use for test
        """
        area['con'].bkgd(' ', curses.A_DIM)
        area['con'].box()
        area['con'].addstr(0, area['w'] // 2 - (len(area['name']) // 2), area['name'], curses.color_pair(curses_wrapper.COLORS[fcolor]['n']))
        for i in range(area['h']):
            area['con'].addstr(i, 0, str(i + 1))
