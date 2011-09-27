"""
map.py

RogueWarts map.

A level in the game's world must have an associated map, which is
defined in here.

  tuple DEF_MAP_DIMS : default maximum dimensions for the map.

  map DUNG_ROOM_LIMS : limit constants for rooms (currently max, min
                       dims and total num).

  class MAPTYPES     : holds dictionaries to define each type of map a
                       level can have.

  class Map          : base class for maps. Holds the basic attributes. A map
                       class may inherit from this one, or at least
                       duck-type its attributes. Also, it must
                       duck-type some basic methods.

  class Dungeon      : 'ADOM' dungeon map.

  class Dungeon2     : 'Rogue' dungeon map.

  class Classrooms   : Classrooms map.

  class Classrooms2  : Classrooms map with empty hole in the center.

  class Cave         : Cave/Wood map.

  class Labyrinth    : Labyrinthic corridors map

  class map_util     : Map utilities.
"""

import libtcod.libtcodpy as tcod
import logging
import room

log = logging.getLogger('roguewarts.map')

"""Default maximum size of the map."""
DEF_MAP_DIMS = (200,100)

"""Default limits constants concerning rooms in the map."""
DUNG_ROOM_LIMS = {'max': 30, 'min': 10, 'num': 50}

class MAPTYPES:
    """
    Types for different kind of level maps.

    Defines classrooms, dungeons, caves, woods, labyrinths, ...

    Each type must have:
      name       - a name for the map type and a class implementing map
                   methods
      deftile    - a type of tile to cover all the map by default
      makeparams - parameters dictionary, used when building the map
    """

    # classrooms, side by side, with central hallway
    classrooms   = {'name'       : 'Classrooms',
                    'deftile'    : room.TILETYPES.wall,
                    'makeparams' : None
                    }

    # classrooms, side by side, with hallway at a side surrounding a
    # central geometric empty (maybe with stairs) hole
    classrooms2 = {'name'       : 'Classrooms2',
                   'deftile'    : room.TILETYPES.wall,
                   'makeparams' : None
                   }

    # dungeon with rooms built side by side
    dungeon      = {'name'       : 'Dungeon',
                    'deftile'    : room.TILETYPES.wall,
                    'makeparams' : {'maxrooms'      : DUNG_ROOM_LIMS['num'],
                                    'room_min_size' : DUNG_ROOM_LIMS['min'],
                                    'room_max_size' : DUNG_ROOM_LIMS['max']}
                    }

    # standard 'roguelike' dungeon
    dungeon2    = {'name'       : 'Dungeon2',
                   'deftile'    : room.TILETYPES.wall,
                   'makeparams' : {'maxrooms'      : DUNG_ROOM_LIMS['num'],
                                   'room_min_size' : DUNG_ROOM_LIMS['min'],
                                   'room_max_size' : DUNG_ROOM_LIMS['max']}
                   }

    # a cave
    cave         = {'name'       : 'Cave',
                    'deftile'    : room.TILETYPES.wall,
                    'makeparams' : None
                    }

    # a wood
    wood         = {'name'       : 'Wood',
                    'deftile'    : room.TILETYPES.tree,
                    'makeparams' : None
                    }

    # labyrinth between rooms (instead of standard corridors/hallways)
    labyrinth    = {'name'       : 'Labyrinth',
                    'deftile'    : room.TILETYPES.wall,
                    'makeparams' : None
                    }

    # special map, probably loaded from data file
    special      = {'name'       : 'Special',
                    'deftile'    : room.TILETYPES.wall,
                    'makeparams' : None
                    }

class Map:
    """
    Generic map class for a level in the game.

    When calling make_map method, it always should receive the
    self.mapa, (self.w,self.h) variables, and everything else as
    optional parameters, defined in the make_map method itself (and
    declared in the MAPTYPES dictionaries)

    Methods:
      __init__

    Variables:
      (w,h)
      mapa
      util
      tipo
      rg
      roomgeo
      rooms
    """
    def __init__(self, tipo, rg, roomgeo=room.Rect):
        """
        """
        (self.w, self.h) = DEF_MAP_DIMS
        self.mapa = None
        self.util = map_util()
        self.tipo = tipo
        self.rg = rg           # level-global random number generator
        self.roomgeo = roomgeo # rooms geometrics class for this map

        try:
            self.mapa = [[ room.Tile(tipo['deftile'])
                           for y in range(self.h) ]
                         for x in range(self.w) ]
            self.rooms = self.make_map((self.w,self.h), mapa = self.mapa, **tipo['makeparams'])
        except Exception as e:
            log.critical(str(e))
            raise Exception("ERROR: could not build map")

class Dungeon(Map):
    """
    Builds a dungeon map.

    A dungeon map has rooms side by side divided by walls and
    corridors. Some dungeons generated at ADOM game are the kind of
    map I'm thinking about here.

    #####     ##########
    #...#######...#....#
    #.............#....##
    ########.##...#......
    #.............#....##
    #....######........#
    ######    ##########

    Methods:
      make_map
    """
    def make_map(self):
        """
        Make a dungeon map.
        """
        log.debug("Building a dungeon map")
        return []

class Dungeon2(Map):
    """
    Builds a dungeon map, standard roguelike variation.

    Here, I'm thinking in the classical dungeon from games as Rogue.

    The algorithm for the generation is taken from
    http://roguebasin.roguelikedevelopment.org/index.php/Complete_Roguelike_Tutorial,_using_python%2Blibtcod,_part_3
    (Basically, it generates some random rooms and in between two
    generated rooms, horizontal/vertical rooms connecting them).

    Also, the BSP algorithm may be used instead
    (cf. http://doryen.eptalys.net/articles/bsp-dungeon-generation/),
    or this may be used in some other class ;)

    #####                       ######
    #...#                       #....#
    #...#           #####       #....#
    #...........    #...#       ##.###
    #...#      ....................
    #####           #...#
                    #####

    Methods:
      make_map
    """
    def make_map(self, (width,height), mapa, maxrooms=50, room_min_size=30, room_max_size=10):
        """
        Make a standard roguelike dungeon map.

        Arguments:
          (width, height) - map dimensions
          mapa            - a 2D list which holds room.Tile instances
          maxrooms        - parameter, max number of rooms to be generated
          room_min_size   - parameter, min size for the generated rooms
          room_max_size   - parameter, max size for the generated rooms

        Returns:
          A list of the generated rooms in the map (corridors may be
          generated too, but they are not accounted for).
        """
        rooms = []
        num_rooms = 0

        for r in range(maxrooms):
            # random room width and height
            rw = tcod.random_get_int(self.rg, room_min_size, room_max_size)
            rh = tcod.random_get_int(self.rg, room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = tcod.random_get_int(self.rg, 0, width - rw - 1)
            y = tcod.random_get_int(self.rg, 0, height - rh - 1)

            # "Rect" class makes rectangles easiert to work with
            new_room = self.roomgeo((x, y), (rw, rh))

            # run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.util.fill_rect_room(mapa, new_room, room.TILETYPES.dung_floor)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms > 0:
                    # all rooms after the first
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # draw a coin (random number that is either 0 or 1)
                    if tcod.random_get_int(self.rg, 0, 1) == 1:
                        # first move horizontally, then vertically
                        self.util.create_h_tunnel(mapa, prev_x, new_x, prev_y, room.TILETYPES.dung_floor)
                        self.util.create_v_tunnel(mapa, prev_y, new_y, new_x, room.TILETYPES.dung_floor)
                    else:
                        # first move vertically, then horizontally
                        self.util.create_v_tunnel(mapa, prev_y, new_y, prev_x, room.TILETYPES.dung_floor)
                        self.util.create_h_tunnel(mapa, prev_x, new_x, new_y, room.TILETYPES.dung_floor)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        log.debug("Building a standard 'roguelike' dungeon map")
        log.debug(" Dimensions: (%s,%s)" % (str(width) , str(height)))
        log.debug(" Number of generated rooms: %s" % str(len(rooms)))

        return rooms

class Classrooms(Map):
    """
    Builds a classrooms map.

    The idea behind this type of map is to create a series of rooms
    side by side, divided by central corridors.

    ####..##########
    #..#..#..#.....#
    #..#.....#.....#
    #.....#..#.....#
    ####..######.###
    #..#............
    #...............
    #..#..##.####...
    #..#..#.....#...
    ####..#######..#
    #........#.....#
    #........#.....#
    ################

    Methods:
      make_map
    """
    def make_map(self):
        """
        Make a classroom map.
        """
        log.debug("Building a classrooms map")
        return []

class Classrooms2(Map):
    """
    Builds a (different) classrooms map.

    The idea behind this one is to build some rooms in the periphery,
    surrounding some empty geometric area.

    In this example, surronding an empty rectangular area:

    ######..#####..####
    #....#..#...#..#..#
    #....#..#...#..#..#
    #...........#.....#
    ######..#####..####
    ...................
    ######..     ..####
    #....#..     ..#..#
    #.......     .....#
    ######..     ..####
    ...................
    ######..#####..####
    #....#..#...#..#..#
    #....#..#...#.....#
    #...........#..#..#
    ######..#####..####

    Methods:
      make_map
    """
    def make_map(self):
        """
        Make a classroom type 2 map.
        """
        log.debug("Building a classrooms type 2 map")
        return []

class Cave(Map):
    """
    Builds a cave or wood map.

    Besides the type of monsters/objects generated, the difference
    comes in the type of walls to use. A wood has trees, a cave has
    rock.

    The idea may be implemented using the algorithm described in
    http://doryen.eptalys.net/articles/dungeon-morphing/ , which uses
    a cellular automata to transform a 'standard' dungeon map in to
    something more amorphous.

    ####.######...#######
    ##....###..########..
    ###.######..########.
    ###.#####....########
    ##.####.......#######
    ##..####.......###.##
    ##...#####...####...#
    ##....######.###.....
    #.......##..........#
    ###...###..#####.....
    #####......######...#
    ##################.##

    Methods:
      make_map
    """
    def make_map(self):
        """
        Make a cave/wood map.
        """
        log.debug("Building a cave/wood map")
        return []

class Labyrinth(Map):
    """
    Builds a labyrinth map.

    The idea is to have some rooms, connected with corridors forming
    labyrinths (or no rooms and a whole labyrinth level ;)

    #######...##....#####
    #...###.#.##.##.....#
    #.......#.#...#.#...#
    ######.##.#.#.#.#...#
    ##......#...#.#######

    Methods:
      make_map
    """
    def make_map(self):
        """
        Make a labyritn map.
        """
        log.debug("Building a labyrinth map")
        return []

class map_util:
    """
    Map utilities class.

    Holds some utility methods for generic use in map classes.

    Methods:
      __init__
      fill_rect_room
      create_h_tunnel
      create_v_tunnel
    """
    def __init__(self):
        """
        Initialization...
        """
        pass

    def fill_rect_room(self, mapa, room, tile):
        """
        Fill a rectangular room.

        Goes through the tiles in the rectangle and make them passable
        (leaving a space for wall's surrounding room)
        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                mapa[x][y].tipo = tile

    def create_h_tunnel(self, mapa, x1, x2, y, tile):
        """
        Creates a horizontal tunnel connecting two coordinates.
        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            mapa[x][y].tipo = tile

    def create_v_tunnel(self, mapa, y1, y2, x, tile):
        """
        Creates a vertical tunnel connecting two coordinates.
        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            mapa[x][y].tipo = tile
