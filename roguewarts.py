#!/usr/bin/env python

'''
roguewarts.py

RogueWarts v0.1
jnc
20/jan/2011
'''

import logging, logging.config, ConfigParser
import sys, getopt
import game
import util

log = None
loglevel = logging.INFO

def config_logger(filename = 'roguewarts.log'):
    """Configure logging facility"""
    global log, loglevel
    try:
        logging.config.fileConfig('logging.conf')
    except ConfigParser.NoOptionError:
        fh = logging.handlers.RotatingFileHandler('log/' + filename, "a", maxBytes=1048576, backupCount=10)
        fh.setLevel(loglevel)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        log = logging.getLogger('roguewarts')
        log.addHandler(fh)

class RogueWarts:
    """RogueWarts main class"""
    def __init__(self, uilib = "libtcod", maximize = False, forcedim = False):
        self.initerror = False
        try:
            self.game = game.Game(uilib, maximize, forcedim)
            self.game.new_game()
        except Exception as e:
            log.error(str(e))
            self.initerror = True
            try:
                self.game.terminate()
            except Exception:
                pass
            print str(e)
        
    def run(self):
        """Run the game (main loop)"""
        log.info("ready to go!")
        while self.game.state != game.STATES.EXIT:
            try:
                self.game.update()
            except KeyboardInterrupt:
                pass
            except Exception as e:
                log.error(str(e))
                print str(e)
                break

        self.game.terminate()

def usage():
    """Usage help screen"""
    print 'RogueWarts, the Harry Potter Roguelike Game'
    print 'Usage: python roguewarts.py [PARAMETERS]'
    print ''
    print ' PARAMETERS:'
    print '   -l ui_library_name        : to change UI library name (currently supporting libtcod & curses'
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
    """Help"""
    usage()

def version():
    """Version"""
    print "Roguewarts v0.1 alpha-1"


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
    rw = RogueWarts(library, maximize, forcedim)
    if rw.initerror:
        sys.exit(1)

    rw.run()
    log.info("goodbye!")
