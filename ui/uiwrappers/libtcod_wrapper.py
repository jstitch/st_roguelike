"""
libtcod_wrapper.py
"""

import libtcod.libtcodpy as libtcod
import textwrap
import logging
import util

log = logging.getLogger('roguewarts.curses_wrapper')

LIMIT_FPS = 20

class libtcod_wrapper:
    """'Interface' for using libtcod as UI library."""
    def __init__(self):
        """"Init interface."""
        self.con = None

    def init(self, (width, height), areas, maximize, forcedim=False):
        """
        Intialize interface.

        Returns screen size in (x,y) tuple.
        """
        libtcod.console_set_custom_font(fontFile='data/arial12x12.png', flags=libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

        if forcedim:
            (width, height) = libtcod.sys_get_current_resolution()
            (chw, chh) = libtcod.sys_get_char_size()
            width = (width / chw)
            height = (height / chh)

        libtcod.console_init_root(w=width, h=height, title='Roguewarts', fullscreen=maximize)
        libtcod.sys_set_fps(LIMIT_FPS)

        # consoles
        w = width
        h = height*10//100
        x = 0
        y = 0
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': libtcod.console_new(w, h), 'name': 'messages' }
        areas['messages'] = map_

        w = width*80//100 + (1 if width % 5 != 0 else 0)
        h = height*80//100 + (2 if height % 10 > 5 else 1)
        x = 0
        y = height*10//100
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': libtcod.console_new(w, h), 'name': 'main' }
        areas['main'] = map_

        w = width*20//100
        h = height*80//100 + (2 if height % 10 > 5 else 1)
        x = width*80//100 + (1 if width % 5 != 0 else 0)
        y = height*10//100
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': libtcod.console_new(w, h), 'name': 'playerstats' }
        areas['playerstats'] = map_

        w = width
        h = height*10//100
        x = 0
        y = height*90//100 + 1
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': libtcod.console_new(w, h), 'name': 'gamestats' }
        areas['gamestats'] = map_

        w = width//2
        h = 3*height//4
        x = width//4
        y = height//8
        map_ = { 'w': w, 'h': h, 'x': x, 'y': y, 'con': libtcod.console_new(w, h), 'name': 'inventory' }
        areas['inventory'] = map_

        return (width, height)

    def getareadims(self, area):
        """Get area dimensions."""
        return (area['w'], area['h'])

    def close(self):
        """Terminate."""
        pass

    def is_closed(self):
        """Tells if user closes window."""
        return libtcod.console_is_window_closed()

    def getkey(self):
        """Get a key."""
        key = libtcod.console_check_for_keypress(True)
        if key.vk == libtcod.KEY_NONE:
            return None
        if not key.vk == libtcod.KEY_CHAR:
            return key.vk
        return chr(key.c)

    def flush(self, area):
        """Flush screen."""
        libtcod.console_blit(area['con'],
                             0, 0, area['w'], area['h'],
                             0, area['x'], area['y'])
        libtcod.console_flush()

    def message(self, queue, mess_area):
        """Display message queue in the message area."""
        libtcod.console_clear(mess_area['con'])

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
                libtcod.console_set_foreground_color(mess_area['con'], getcolorbyname(qlines[i].properties['color']))
                libtcod.console_print_left(mess_area['con'], 0, mess_area['h'] - i - 1, libtcod.BKGND_NONE, qlines[i].message)
                self.flush(mess_area)
            except IndexError:
                break

    def render(self, level, x, y, minx, miny, maxx, maxy, main_area):
        """Render current level."""
        libtcod.console_clear(main_area['con'])

        map_ = level.mapa

        # determine console coordinates to begin rendering according to map size
        (conx, cony) = ((main_area['w'] - map_.w)//2 if map_.w < main_area['w'] else 0,
                        (main_area['h'] - map_.h)//2 if map_.h < main_area['h'] else 0)

        # draw map tiles
        for my, cy in map(None, range(miny, maxy), range(cony, map_.h + cony)):
            for mx, cx in map(None, range(minx, maxx), range(conx, map_.w + conx)):
                visible = True # libtcod.map_is_in_fov(fov_map, x, y)
                try:
                    tile = map_.mapa[mx][my]
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
                    libtcod.console_set_back(main_area['con'], cx, cy, getcolorbyname(tile.tipo['color']), libtcod.BKGND_SET)
                    libtcod.console_set_back(main_area['con'], conx + x - minx, cony + y - miny, getcolorbyname('red'), libtcod.BKGND_SET)
                    # since now it's visible, mark it as explored
                    tile.explored = True

        # draw objects in map...

        # blit contents
        self.flush(main_area)

    def test(self, areas):
        """Test routine."""
        # blit messages
        self.test_area(areas['messages'], libtcod.red, libtcod.black)

        # blit main
        self.test_area(areas['main'], libtcod.yellow, libtcod.black)

        # blit playerstats
        self.test_area(areas['playerstats'], libtcod.green, libtcod.black)

        # blit gamestats
        self.test_area(areas['gamestats'], libtcod.blue, libtcod.black)

        # blit inventory
        self.test_area(areas['inventory'], libtcod.orange, libtcod.black)

        libtcod.console_credits()

    def test_area(self, area, fcolor, bcolor):
        """Draw routines to test game areas."""
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
    """Get libtcod color from name."""
    return getattr(libtcod, strcolorname, libtcod.white)
