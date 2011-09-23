'''
map.py
'''

import libtcod.libtcodpy as tcod
import logging

log = logging.getLogger('roguewarts.map')

# default maximum size of the map
DEF_MAP_WIDTH = 200
DEF_MAP_HEIGHT = 100

# parameters for dungeon generation
DUNG_ROOM_MAX_SIZE = 30
DUNG_ROOM_MIN_SIZE = 10
DUNG_MAX_ROOMS = 50

class Rect:
    """Rectangle, basic unit for rooms"""
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    # get center coordinates
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    # returns True if this rectangle intersects with another one
    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class Circle:
    def __init__():
        pass

class Hexag:
    def __init__():
        pass

class TILETYPES:
    """Types for the tiles in the map"""
    # walls
    wall   = {'name': 'wall', 'char': '#', 'color': 'dark_blue', 'nv_color': '', 'block_pass': True, 'block_sight': True}
    tree   = {'name': 'tree', 'char': '#', 'color': 'dark_green', 'nv_color': '', 'block_pass': True, 'block_sight': True}
    window = {'name': 'window', 'char': '=', 'color': 'light_cyan', 'nv_color': '', 'block_pass': True, 'block_sight': False}

    # floors
    dung_floor  = {'name': 'floor', 'char': '.', 'color': 'light_yellow', 'nv_color': '', 'block_pass': False, 'block_sight': False}
    stall       = {'name': 'stall', 'char': '-', 'color': 'dark_yellow', 'nv_color': '', 'block_pass': False, 'block_sight': False}
    desk        = {'name': 'desk', 'char': '-', 'color': 'dark_yellow', 'nv_color': '', 'block_pass': False, 'block_sight': False}

class Tile:
    """Tile class, a tile on the map"""
    def __init__(self, type = TILETYPES.wall):
        self.type = type
        # 'explored by the player' status
        self.explored = False

class MAPTYPES:
    """Types for different kind of maps"""
    classrooms   = {'name': 'classrooms',   # classrooms side by side with central hallway
                    'deftile': TILETYPES.wall,
                    'makeparams': None
                    }
    classrooms_2 = {'name': 'classrooms_2', # classrooms side by side with hallway at a side surrounding a central geometric empty (maybe with stairs) hole
                    'deftile': TILETYPES.wall,
                    'makeparams': None
                    }
    dungeon      = {'name': 'dungeon',    # dungeon with rooms side by side
                    'deftile': TILETYPES.wall,
                    'makeparams': {'maxrooms': DUNG_MAX_ROOMS, 'room_min_size': DUNG_ROOM_MIN_SIZE, 'room_max_size': DUNG_ROOM_MAX_SIZE}
                    }
    dungeon_2    = {'name': 'dungeon_2',      # standard 'roguelike' dungeon
                    'deftile': TILETYPES.wall,
                    'makeparams': {'maxrooms': DUNG_MAX_ROOMS, 'room_min_size': DUNG_ROOM_MIN_SIZE, 'room_max_size': DUNG_ROOM_MAX_SIZE}
                    }
    cave         = {'name': 'cave',         # a cave
                    'deftile': TILETYPES.wall,
                    'makeparams': None
                    }
    wood         = {'name': 'wood',         # a wood
                    'deftile': TILETYPES.tree,
                    'makeparams': None
                    }
    labyrinth    = {'name': 'labyrinth',    # labyrinth between rooms
                    'deftile': TILETYPES.wall,
                    'makeparams': None
                    }
    special      = {'name': 'special',      # special map, probably loaded from file
                    'deftile': TILETYPES.wall,
                    'makeparams': None
                    }

class Map:
    """Map class for a level in the game"""
    def __init__(self, type, rg, roomgeo=Rect):
        self.w = DEF_MAP_WIDTH
        self.h = DEF_MAP_HEIGHT
        self.map = None
        self.util = map_util()
        self.type = type
        self.rg = rg           # level-global random number generator
        self.roomgeo = roomgeo # rooms geometrics class for this map

        try:
            self.map = [[ Tile(type['deftile'])
                          for y in range(self.h) ]
                        for x in range(self.w) ]
            self.rooms = getattr(self, "make_" + type['name'] + "_map")(map = self.map, width = self.w, height = self.h, **type['makeparams'])
        except Exception as e:
            log.critical(str(e))
            raise Exception("ERROR: could not build map")

    def make_dungeon_map(self):
        """Make a dungeon map"""
        log.debug("Building a dungeon map")
        return []

    def make_dungeon_2_map(self, map, width, height, maxrooms, room_min_size, room_max_size):
        """Make a standard roguelike dungeon map"""
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
            new_room = self.roomgeo(x, y, rw, rh)

            # run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.util.fill_rect_room(map, new_room, TILETYPES.dung_floor)

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
                        self.util.create_h_tunnel(map, prev_x, new_x, prev_y, TILETYPES.dung_floor)
                        self.util.create_v_tunnel(map, prev_y, new_y, new_x, TILETYPES.dung_floor)
                    else:
                        # first move vertically, then horizontally
                        self.util.create_v_tunnel(map, prev_y, new_y, prev_x, TILETYPES.dung_floor)
                        self.util.create_h_tunnel(map, prev_x, new_x, new_y, TILETYPES.dung_floor)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        log.debug("Building a standard 'roguelike' dungeon map")
        log.debug(" Dimensions: (%s,%s)" % (str(width) , str(height)))
        log.debug(" Number of generated rooms: %s" % str(len(rooms)))
        return rooms

    def make_classrooms_map(self):
        """Make a classroom map"""
        log.debug("Building a classrooms map")
        return []

    def make_classrooms_2_map(self):
        """Make a classroom type 2 map"""
        log.debug("Building a classrooms type 2 map")
        return []

    def make_cave_map(self):
        """Make a cave/wood map"""
        log.debug("Building a cave/wood map")
        return []

    def make_labyrinth_map(self):
        """Make a labyritn map"""
        log.debug("Building a labyrinth map")
        return []

class map_util:
    """Map utilities"""
    def __init__(self):
        pass

    def fill_rect_room(self, map, room, tile):
        """Fill a rectangular room"""
        # go through the tiles in the rectangle and make them passable (leaving
        # space for wall surrounding room)
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                map[x][y].type = tile

    # Carve horizontal tunnel
    def create_h_tunnel(self, map, x1, x2, y, tile):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            map[x][y].type = tile

    # Carve vertical tunnel
    def create_v_tunnel(self, map, y1, y2, x, tile):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            map[x][y].type = tile
