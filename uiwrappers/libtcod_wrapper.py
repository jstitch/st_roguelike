'''
libtcod_wrapper.py
'''

import libtcod.libtcodpy as libtcod
import textwrap
import logging
import util

log = logging.getLogger('roguewarts.curses_wrapper')

LIMIT_FPS = 20

class libtcod_wrapper:
    """'Interface' for using libtcod as UI library"""
    def __init__(self):
        self.con = None

    def init(self, width, height, maximize, forcedim=False):
        """Intialization. Returns screen size in (x,y) tuple"""
        libtcod.console_set_custom_font(fontFile='data/arial12x12.png', flags=libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

        if forcedim:
            (width, height) = libtcod.sys_get_current_resolution()
            (chw, chh) = libtcod.sys_get_char_size()
            width = (width / chw)
            height = (height / chh)

        libtcod.console_init_root(w=width, h=height, title='Roguewarts', fullscreen=maximize)
        libtcod.sys_set_fps(LIMIT_FPS)

        # main console
        self.main = { 'con': None, 'name': '', 'w': 0, 'h': 0, 'x': 0, 'y': 0 }
        # messages console
        self.messages = { 'con': None, 'name': '', 'w': 0, 'h': 0, 'x': 0, 'y': 0 }
        # player stats console
        self.playerstats = { 'con': None, 'name': '', 'w': 0, 'h': 0, 'x': 0, 'y': 0 }
        # game stats console
        self.gamestats = { 'con': None, 'name': '', 'w': 0, 'h': 0, 'x': 0, 'y': 0 }
        # inventory console
        self.inventory = { 'con': None, 'name': '', 'w': 0, 'h': 0, 'x': 0, 'y': 0 }

        # consoles
        w = width
        h = height*10//100
        x = 0
        y = 0
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': libtcod.console_new(w, h), 'name': 'messages' }
        self.messages = map_

        w = width*80//100 + (1 if width % 5 != 0 else 0)
        h = height*80//100 + (2 if height % 10 > 5 else 1)
        x = 0
        y = height*10//100
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': libtcod.console_new(w, h), 'name': 'main' }
        self.main = map_

        w = width*20//100
        h = height*80//100 + (2 if height % 10 > 5 else 1)
        x = width*80//100 + (1 if width % 5 != 0 else 0)
        y = height*10//100
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': libtcod.console_new(w, h), 'name': 'playerstats' }
        self.playerstats = map_

        w = width
        h = height*10//100
        x = 0
        y = height*90//100 + 1
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': libtcod.console_new(w, h), 'name': 'gamestats' }
        self.gamestats = map_

        w = width//2
        h = 3*height//4
        x = width//4
        y = height//8
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': libtcod.console_new(w, h), 'name': 'inventory' }
        self.inventory = map_

        return (width, height)

    def getareadims(self):
        """Get main area dimensions"""
        return (self.main['w'], self.main['h'])

    def close(self):
        """Termination"""
        pass

    def is_closed(self):
        """If user closes window"""
        return libtcod.console_is_window_closed()

    def getkey(self):
        """Get a key"""
        key = libtcod.console_check_for_keypress(True)
        if key.vk == libtcod.KEY_NONE:
            return None
        if not key.vk == libtcod.KEY_CHAR:
            return key.vk
        return chr(key.c)

    def flush(self, area):
        """Flush screen"""
        if area == 'all' or area == 'map':
            libtcod.console_blit(self.main['con'],
                                 0, 0, self.main['w'], self.main['h'],
                                 0, self.main['x'], self.main['y'])
        if area == 'all' or area == 'messages':
            libtcod.console_blit(self.messages['con'],
                                 0, 0, self.messages['w'], self.messages['h'],
                                 0, self.messages['x'], self.messages['y'])
        if area == 'all' or area == 'stats':
            libtcod.console_blit(self.playerstats['con'],
                                 0, 0, self.playerstats['w'], self.playerstats['h'],
                                 0, self.playerstats['x'], self.playerstats['y'])
            libtcod.console_blit(self.gamestats['con'],
                                 0, 0, self.gamestats['w'], self.gamestats['h'],
                                 0, self.gamestats['x'], self.gamestats['y'])
        if area == 'all' or area == 'inventory':
            libtcod.console_blit(self.inventory['con'],
                                 0, 0, self.inventory['w'], self.inventory['h'],
                                 0, self.inventory['x'], self.inventory['y'])
        libtcod.console_flush()

    def message(self, queue):
        """Display message queue in the message area"""
        libtcod.console_clear(self.messages['con'])

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
                libtcod.console_set_foreground_color(self.messages['con'], getcolorbyname(qlines[i].properties['color']))
                libtcod.console_print_left(self.messages['con'], 0, self.messages['h'] - i - 1, libtcod.BKGND_NONE, qlines[i].message)
                self.flush('messages')
            except IndexError:
                break

    def render(self, level, x, y, minx, miny, maxx, maxy):
        """Render current level level"""
        libtcod.console_clear(self.main['con'])

        map_ = level.map

        # determine console coordinates to begin rendering according to map size
        (conx, cony) = ((self.main['w'] - map_.w)//2 if map_.w < self.main['w'] else 0,
                        (self.main['h'] - map_.h)//2 if map_.h < self.main['h'] else 0)

        # draw map tiles
        for my, cy in map(None, range(miny, maxy), range(cony, map_.h + cony)):
            for mx, cx in map(None, range(minx, maxx), range(conx, map_.w + conx)):
                visible = True # libtcod.map_is_in_fov(fov_map, x, y)
                try:
                    tile = map_.map[mx][my]
                except Exception as e:
                    continue
                # it's out of the player's FOV, player will see it only if explored
                if not visible:
                    if tile.explored:
                        # draw map tile with char/color <- modifications for explored/not visible
                        pass
                # it's visible
                else:
                    # draw map tile with char/color <- as is since it is visible
                    libtcod.console_set_back(self.main['con'], cx, cy, getcolorbyname(tile.type['color']), libtcod.BKGND_SET)
                    libtcod.console_set_back(self.main['con'], conx + x - minx, cony + y - miny, getcolorbyname('red'), libtcod.BKGND_SET)
                    # since now it's visible, mark it as explored
                    tile.explored = True

        # draw objects in map...

        # blit contents
        self.flush('map')

    def test(self):
        """Test routine"""
        # blit messages
        self.test_area(self.messages, libtcod.red, libtcod.black)

        # blit main
        self.test_area(self.main, libtcod.yellow, libtcod.black)

        # blit playerstats
        self.test_area(self.playerstats, libtcod.green, libtcod.black)

        # blit gamestats
        self.test_area(self.gamestats, libtcod.blue, libtcod.black)

        # blit inventory
        self.test_area(self.inventory, libtcod.orange, libtcod.black)

        libtcod.console_credits()

    def test_area(self, area, fcolor, bcolor):
        """Draw routines to test game areas"""
        libtcod.console_set_background_color(area['con'], bcolor)
        libtcod.console_set_foreground_color(area['con'], fcolor)
        libtcod.console_clear(area['con'])
        libtcod.console_print_frame(area['con'], 0, 0, area['w'], area['h'], False, None, area['name'] + ": " + str(area))
        for i in range(area['h']):
            libtcod.console_print_left(area['con'], 0, i, libtcod.BKGND_NONE, str(i + 1))
        libtcod.console_blit(area['con'],
                             0, 0, area['w'], area['h'],
                             0, area['x'], area['y'])

def getcolorbyname(strcolorname):
    """Get libtcod color from name"""
    return getattr(libtcod, strcolorname, libtcod.white)
