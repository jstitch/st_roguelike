"""
uiwrappers package

UI wrappers for RogueLike.

Currently supported:

  libtcod_wrapper for libtcod* based graphics support

  curses_wrapper  for ncurses** support


* libtcod is a very complete library, which not only supports graphics
routines, but also many other useful utilities for roguelike games
development. The wrapper only includes graphics routines, while the
rest of the game may use any other part of the library for the
roguelike support, independent of the UI issues.

** curses wrapper is intended to run even on a remote SSH (or telnet)
   session for the game. But since libtcod is used in many other parts
   of the game, and since current libtcod version (1.5.0) initializes
   the graphics part along with any other use of the library, then a
   remote session cannot run the game, throwing an error, since some
   initializations by libtcod require a graphics environment to be run
   locally.

   So, some changes were made to the standard distributed libtcod
   library, so that graphics won't get initialized at the very
   beginning when using any other functionality, allowing a remote
   session of the game to run cleanly. There is a patch to achieve
   this for libtcod version 1.5.0 inside the libtcod directory.

   If you do not intend to run RogueLike changes to libtcod are
   needed, as long as the graphics environment for the OS running the
   game is enabled (X Window in Unix environments, Windows and MacOSX
   have this enabled by default).


An UI wrapper should consist of a class (whose name should be the same
as the module containing it, a la Java) so that ui.py may find and it
load it correctly. The UI wrapper is the only one allowed to call
library-dependent routines to interact with a particular input/output
method (which may be keyboard, mouse, graphics, sound, etc.) The ui
class in the ui.py module is the only one allowed to use this wrappers
by calling its duck-typed methods, this way hiding all the UI
library-specific logic in the game.

These are the methods that the UI wrapper should have:

  __init__    class constructor, for variables creation, etc.

  init        initializes interface: UI init, screen dimensions, input init,
              game areas init (main area, messages area, player stats
              area, game stats area, inventory area). Receives any
              additional parameters for the UI

              Should return a tuple with screen size (y,x)

  getareadims returns a tuple with the main game area dimensions

  close       terminates the UI

  is_closed   tells if UI is requested to be closed by user

  getkey      returns an input key by the user. Must catch the key pressed
              in a non-blocking way. ASCII code for alphanumeric keys,
              special mapped keys for control keys. It uses libtcod
              library to map the library-dependent code to a libtcod
              similar one (see curses_wrapper.KEY_MAP for an example)

  flush       flushes screen or an specific area of it

  message     displays a message in the message area, taken from a given
              message queue

  render      renders current level in the main area. It receives the level
              to be drawn, the coordinates for the currently character
              being played by the user and, since the level dimensions
              usually won't be the same as the main area dimensions, the
              coordinates for a box in the level to be drawn inside the
              main area, usually centered.

  test        test routine for the wrapper. It usually draws some frames around
              each area and other specific information


The wrapper also should know how to manage a dictionary of 'areas',
which define each area in the screen. The definition is:

area = {'con' : None, # a manager for the area, UI library specific
        'name': '',   # the name (id) of the area
        'w'   : 0,    # width of the area in characters
        'h'   : 0,    # height of the area in characters
        'x'   : 0,    # the x coordinate (in characters) of the top
                      # left corner of the area
        'y': 0        # the y coordinate (in characters) of the top
                      # left corner of the area
        }

More info on this areas on ui.py and each uiwrappers source code:

Areas:
  main         - game map
  messages     - messages for the user from the game
  player stats - stats for the current player
  game stats   - stats for the overall game
  inventory    - where the inventory appears

The default layout of the screen areas (at least for the libtcod and
curses wrappers) is as follows:

+--------------------------------------------------------+
| messages                                               |
+----------------------------------------------+---------+
| main area                                    | player  |
|                                              |  stats  |
|           +----------------------------+     |         |
|           | inventory                  |     |         |
|           |                            |     |         |
|           |                            |     |         |
|           |                            |     |         |
|           |                            |     |         |
|           |                            |     |         |
|           |                            |     |         |
|           |                            |     |         |
|           +----------------------------+     |         |
|                                              |         |
+----------------------------------------------+---------+
| game stats                                             |
+--------------------------------------------------------+
"""
