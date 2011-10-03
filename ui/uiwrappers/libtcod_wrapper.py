"""
libtcod_wrapper.py

libtcod graphical UI library wrapper for RogueWarts.

For RogueWarts UI purposes, a class is a UI wrapper if it implements
certain methods. Look for the class documentation to see what methods
they are.

  integer LIMIT_FPS : frames per second constant. Since input is
                      non-blocking, this number is required for
                      libtcod consoles. This would allow, in theory, a
                      real time game too.

  class libtcod_wrapper : implementation for RogueWarts UI using
                          libtcod

  func getcolorbyname : gets a libtcod color from a string name
"""

import libtcod.libtcodpy as libtcod
import textwrap
import logging

import game.util as util

log = logging.getLogger('roguewarts.curses_wrapper')

LIMIT_FPS = 20

class libtcod_wrapper:
    """
    Implementation for using libtcod as UI library.

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
      con          - libtcod console representing the whole screen
    """
    def __init__(self):
        """
        Initialize variables.
        """
        self.con = None

    def init(self, (width, height), areas, maximize, forcedim=False):
        """
        Properly initialize UI wrapper.

        Initializes libtcod console with:
         -root console for game window
         -font to use
         -FPS

        Also determines screen size.

        Finally, initializes each game area as a libtcod console.

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

        Since libtcod doesn't need any closing routines, it just
        passes.
        """
        pass

    def is_closed(self):
        """
        Tells if user closes window.

        Curses has no 'windows' interface for the user to close via
        some button, external to the mechanisms of the game itself (as
        in other UIs, where maybe an X button or Alt-F4 key
        combination allows to close the program), so it always returns
        False.

        Return:
          boolean telling if UI has been closed by the user.
        """
        return libtcod.console_is_window_closed()

    def getkey(self):
        """
        Get a key.

        Manages user input, using non-blocking methods.

        Returns:
          ASCII code for an alphanumeric key, else libtcod code
        """
        key = libtcod.console_check_for_keypress(True)
        if key.vk == libtcod.KEY_NONE:
            return None
        if not key.vk == libtcod.KEY_CHAR:
            return key.vk
        return chr(key.c)

    def flush(self, area):
        """
        Flush screen area.

        Arguments:
          area : the area to be flushed
        """
        libtcod.console_blit(area['con'],
                             0, 0, area['w'], area['h'],
                             0, area['x'], area['y'])
        libtcod.console_flush()

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
        """
        Test routine.

        Draws some test things in each area.

        Arguments:
          areas : the areas dictionary
        """
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
        """
        Draw routines to test game areas.

        Draws some test things in a specific area.

        Arguments:
          area   : area to be tested
          fcolor : foreground color to use for test
          bcolor : background color to use for test
        """
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
    """
    Get libtcod color from name.
    
    Arguments:
      strcolorname : the name of the color to retrieve from libtcod
                     library

    Returns:
      libtcod color
    """
    return getattr(libtcod, strcolorname, libtcod.white)
