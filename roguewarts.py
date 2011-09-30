#!/usr/bin/env python
"""
roguewarts.py

RogueWarts, the Harry Potter Roguelike Game

RogueWarts may use different graphical libraries for displaying the
game. Curses is supported, but also libtcod, which BTW also gives
support to the engine behind the game itself.

Usage: python roguewarts.py [PARAMETERS]

PARAMETERS:

  -l ui_library_name        : to change UI library name (currently supporting
                              libtcod (default) & curses)

  --library=ui_library_name : same as above

  --maximize                : maximize display in screen

  --forcedim                : forces display size to maximum allowed by current
                              screen (allows low-res screens to run
                              the game - warning, very low res might
                              not render things well)

  --debug                   : enable debug mode

  -v                        : game version

  -h | -? | --help          : help screen



This module also includes the following:

  class Roguewarts           : RogueWarts main class.

  function config_logger     : Configures the logging facitliy.

  function usage             : Prints usage screen.

  function help              : Prints game help and exits

  function version           : Prints game current version information.

  main routine


RogueWarts, the Harry Potter Roguelike Game
Copyright (C) 2011 Javier Novoa C.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or any
later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

JNC - jstitch@gmail.com
20/jan/2011
"""

import logging, logging.config, ConfigParser
import sys, getopt, os, traceback as tbck

import game.game as game
import game.util as util

GAME_NAME = "RogueWarts"
GAME_VERSION = "0.1 alpha-1"

log = None
loglevel = logging.INFO

def config_logger(filename = 'roguewarts.log'):
    """
    Configure logging facility.

    Reads logging.conf for configurations.

    Arguments:
      filename : the name of the file to store the log into. Default:
                 'roguewarts.log'
    """
    global log, loglevel
    try:
        if not os.path.exists('log/'):
            os.mkdir('log/')
        logging.config.fileConfig('logging.conf')
    except ConfigParser.NoOptionError:
        fh = logging.handlers.RotatingFileHandler('log/' + filename, "a", maxBytes=1048576, backupCount=10)
        fh.setLevel(loglevel)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        log = logging.getLogger('roguewarts')
        log.addHandler(fh)

class RogueWarts:
    """
    RogueWarts main class.

    Methods:
      __init__
      run
      finish

    Variables:
      game - the game engine
    """
    def __init__(self, uilib = "libtcod", uiparams = (False, False)):
        """
        Initialize the game engine, UI included.

        Arguments:
          uilib    : the name of the UI library to use. Default: 'libtcod'
          uiparams : tuple with parameters for the UI lib (see ui.py
                     doc for more info). Default: (False, False)
        """
        try:
            self.game = game.Game(uilib, uiparams)
        except Exception as e:
            log.error(tbck.format_exc())
            raise util.RoguewartsException("initerror:" + str(e))
        
    def run(self):
        """
        Run the game (main loop).

        A game loop calls the iterate() method of the Game class. This
        method calls some other method which may vary, according to
        where in the game we are: player configuration? main game?
        etc.

        The loop is supposed to cleanly terminate when the game
        reaches an EXIT state.
        """
        log.info("ready to go!")
        while self.game.state != game.STATES['EXIT']:
            try:
                self.game.iterate()
            except KeyboardInterrupt:
                pass
            except Exception as e:
                log.error(tbck.format_exc())
                print str(e)
                break

    def finish(self):
        """
        Finish the game cleanly.
        """
        try:
            self.game.terminate()
        except Exception as e:
            pass

def usage():
    """
    Print usage help screen.
    """
    print 'RogueWarts, the Harry Potter Roguelike Game'
    version()
    print ''
    print 'Usage: python roguewarts.py [PARAMETERS]'
    print ''
    print ' PARAMETERS:'
    print '   -l ui_library_name        : to change UI library name (currently supporting libtcod (default) & curses)'
    print '   --library=ui_library_name : same as above'
    print '   --maximize                : maximize display in screen'
    print '   --forcedim                : forces display size to maximum allowed by current screen'
    print '                               (allows low-res screens to run the game - warning, very low res might not render things well)'
    print '   --debug                   : enable debug mode'
    print '   -v                        : game version'
    print '   -h | -? | --help          : this help screen'
    print ''
    print 'If you find any bugs, please report them to jstitch@gmail.com. Make sure to include information of what were you doing at the moment of the crash, any message the game sent to you, and if possilbe include any generated files that may give some clues of what had happened (logs/saves/etc.). Priority is given to detailed reports, and preferably to those including clues at where in the code the problem might be. Any patches and fixes are most welcomed!'

def help():
    """
    Print help.
    """
    usage()

def version():
    """
    Print version.
    """
    print "version", GAME_VERSION
    print GAME_NAME, "is under the GPLv3 License"


#### MAIN ROUTINE ####
if __name__ == '__main__':
    library = "libtcod"
    maximize = False
    forcedim = False

    # command line args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "?hl:v", ['library=', 'help', 'debug', 'verbose', 'maximize', 'forcedim'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-l", "--library"):
            library = arg
        elif opt in ("--maximize"):
            maximize = True
        elif opt in("--forcedim"):
            forcedim = True
        elif opt in ("-?", "-h", "--help"):
            help()
            sys.exit()
        elif opt in ("-v"):
            version()
            sys.exit()
        elif opt in ("--debug"):
            loglevel = logging.DEBUG
            util.debug = True
        else:
            assert False, "unhandled option"

    # logging
    config_logger()
    log.info("hullo!")

    # roguewarts
    try:
        rw = RogueWarts(library, (maximize, forcedim))
    except util.RoguewartsException as e:
        try:
            rw.finish()
        except Exception:
            pass
        print str(e)
        sys.exit(1)

    rw.run()
    rw.finish()
    log.info("goodbye!")
