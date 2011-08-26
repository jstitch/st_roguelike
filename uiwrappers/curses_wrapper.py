'''
curses_wrapper.py
'''

import curses
import textwrap
import libtcod.libtcodpy as libtcod
import logging
import util

log = logging.getLogger('roguewarts.curses_wrapper')

# In theory, using curses as UI library, may allow to run the game in remote
# SSH/telnet sessions. BUT libtcod (which is also used for other
# game-logic/non-graphic thigs), requires the game to be run locally. At the
# roguecentral forums, I've been searching for a possible solution to
# this. Right now libtcod won't allow remote running, but recompiling it with
# certain changes in the libtcod sourcode may allow this (note that this would
# only be necessary in the 'server' on which the game would run).
class curses_wrapper:
    """'Interface' for using curses as UI library"""

    # http://docs.python.org/library/curses.html#constants
    KEY_MAP = {
        curses.KEY_LEFT  : libtcod.KEY_LEFT,
        curses.KEY_RIGHT : libtcod.KEY_RIGHT,
        curses.KEY_UP    : libtcod.KEY_UP,
        curses.KEY_DOWN  : libtcod.KEY_DOWN,
        27               : libtcod.KEY_ESCAPE
        }

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
        self.scr = None

    def init(self, minwidth, minheight, maximize=False, forcemindims=False):
        """Intialization. Returns screen size in (y,x) tuple."""
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

        # main console
        self.main = { 'con': None, 'w': 0, 'h': 0, 'x': 0, 'y': 0 }
        # messages console
        self.messages = { 'con': None, 'w': 0, 'h': 0, 'x': 0, 'y': 0 }
        # player stats console
        self.playerstats = { 'con': None, 'w': 0, 'h': 0, 'x': 0, 'y': 0 }
        # game stats console
        self.gamestats = { 'con': None, 'w': 0, 'h': 0, 'x': 0, 'y': 0 }
        # inventory console
        self.inventory = { 'con': None, 'w': 0, 'h': 0, 'x': 0, 'y': 0 }

        # consoles
        w = self.maxx
        h = self.maxy*10//100
        x = 0
        y = 0
        win = self.scr.subwin(h, w, y, x)
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': win, 'name': 'messages' }
        self.messages = map_

        w = self.maxx*80//100 + (self.maxx % 5 != 0 and 1 or 0)
        h = self.maxy*80//100 + (self.maxy % 10 > 5 and 1 or 0)
        x = 0
        y = self.maxy*10//100
        win = self.scr.subpad(h, w, y, x)
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': win, 'name': 'main' }
        self.main = map_

        w = self.maxx*20//100
        h = self.maxy*80//100 + (self.maxy % 10 > 5 and 1 or 0)
        x = self.maxx*80//100 + (self.maxx % 5 != 0 and 1 or 0)
        y = self.maxy*10//100
        win = self.scr.subwin(h, w, y, x)
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': win, 'name': 'playerstats' }
        self.playerstats = map_

        w = self.maxx
        h = self.maxy*10//100
        x = 0
        y = self.maxy*90//100
        win = self.scr.subwin(h, w, y, x)
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': win, 'name': 'gamestats' }
        self.gamestats = map_

        w = self.maxx//2
        h = 3*self.maxy//4
        x = self.maxx//4
        y = self.maxy//8
        win = self.scr.subwin(h, w, y, x)
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': win, 'name': 'inventory' }
        self.inventory = map_

        return (self.maxx,self.maxy)

    def getareadims(self):
        """Get main area dimensions"""
        return (self.main['w'], self.main['h'])

    def close(self):
        """Termination"""
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def is_closed(self):
        """If user closes window"""
        return False

    def getkey(self):
        """Get a key"""
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
        """Flush screen"""
        if area == 'all':
            self.flush('messages')
            self.flush('map')
            self.flush('stats')
            self.flush('inventory')
            self.scr.refresh()

        elif area == 'messages':
            self.messages['con'].refresh()

        elif area == 'map':
            self.main['con'].refresh()

        elif area == 'stats':
            self.playerstats['con'].refresh()
            self.gamestats['con'].refresh()

        elif area == 'inventory':
            self.inventory['con'].refresh()

    def message(self, queue):
        """Display a message queue in the message area"""
        self.messages['con'].clear()

        qmess = []
        for i in range(self.messages['h']):
            try:
                qmess.append(queue[(i + 1) * -1])
            except IndexError:
                break

        qlines = []
        for mess in qmess:
            str_lines = textwrap.wrap(mess.message, self.messages['w'])
            qlines.extend([util.Message(line, mess.properties) for line in str_lines])

        for i in range(self.messages['h']):
            try:
                self.messages['con'].addstr(self.messages['h'] - i - 1,
                                            0,
                                            qlines[i].message,
                                            curses.color_pair(curses_wrapper.COLORS[qlines[i].properties['color']]['n']))
            except IndexError:
                break

        self.flush('messages')

    def render(self, level, x, y, minx, miny, maxx, maxy):
        """Render current level"""
        self.main['con'].clear()

        map_ = level.map

        # determine console coordinates to begin rendering according to map size
        (conx, cony) = (map_.w < self.main['w'] and (self.main['w'] - map_.w)//2 or 0,
                        map_.h < self.main['h'] and (self.main['h'] - map_.h)//2 or 0)

        # draw map tiles
        if util.debug:
            c = 0
        for my, cy in map(None, range(miny, maxy), range(cony, map_.h + cony)):
            for mx, cx in map(None, range(minx, maxx), range(conx, map_.w + conx)):
                visible = True # libtcod.map_is_in_fov(fov_map, x, y)
                try:
                    tile = map_.map[mx][my]
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
                        self.main['con'].addstr(cy, cx, tile.type['char'],
                                                curses.color_pair(curses_wrapper.COLORS[tile.type['color']]['n']))
                        self.main['con'].addstr(cony + y - miny, conx + x - minx, '@',
                                                curses.color_pair(curses_wrapper.COLORS['red']['n']))
                    except Exception as e:
                        pass
                    # since now it's visible, mark it as explored
                    tile.explored = True
        if util.debug:
            log.debug("aparecio none %d veces" % c)

        self.flush('map')

    def test(self):
        """Test routine"""
        self.scr.clear()

        # blit messages
        self.test_area(self.messages, 'red', '')

        # blit main
        self.test_area(self.main, 'yellow', '')

        # blit playerstats
        self.test_area(self.playerstats, 'green', '')

        # blit gamestats
        self.test_area(self.gamestats, 'blue', '')

        # blit inventory
        self.test_area(self.inventory, 'cyan', '')

        self.scr.addstr(self.maxy//2, self.maxx//2, curses.__name__)

    def test_area(self, area, fcolor, bcolor):
        """Draw routines to test game areas"""
        area['con'].bkgd(' ', curses.A_DIM)
        area['con'].box()
        area['con'].addstr(0, area['w'] // 2 - (len(area['name']) // 2), area['name'], curses.color_pair(curses_wrapper.COLORS[fcolor]['n']))
        for i in range(area['h']):
            area['con'].addstr(i, 0, str(i + 1))
