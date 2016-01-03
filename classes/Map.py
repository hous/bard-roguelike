import libtcodpy as libtcod
import Constants as C
from Rect import Rect

class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Map(object):
    def __init__(self, console, width, height, config = None):
        self.console = console
        self.width = width
        self.height = height
        self.config = config
        self.starting_coords = { 'x' : 0, 'y' : 0 }
        self.map = [[ Tile(True)
            for y in range(self.height) ]
                for x in range(self.width) ]

        rooms = []
        num_rooms = 0

        for r in range(C.DUNGEON_MAX_ROOMS):
            #random width and height
            w = libtcod.random_get_int(0, C.DUNGEON_ROOM_MIN_SIZE, C.DUNGEON_ROOM_MAX_SIZE)
            h = libtcod.random_get_int(0, C.DUNGEON_ROOM_MIN_SIZE, C.DUNGEON_ROOM_MAX_SIZE)
            #random position without going out of the boundaries of the map
            x = libtcod.random_get_int(0, 0, self.width - w - 1)
            y = libtcod.random_get_int(0, 0, self.height - h - 1)

            #"Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            #run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                #this means there are no intersections, so this room is valid

                print(new_room)
                #"paint" it to the map's tiles
                self.create_room(new_room)

                #center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    #this is the first room, where the player starts at
                    self.starting_coords['x'] = new_x
                    self.starting_coords['y'] = new_y
                else:
                    #all rooms after the first:
                    #connect it to the previous room with a tunnel

                    #center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms-1].center()

                    #draw a coin (random number that is either 0 or 1)
                    if libtcod.random_get_int(0, 0, 1) == 1:
                        #first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        #first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                #finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1


        # Testing
        self.map[30][22].blocked = True
        self.map[30][22].block_sight = True
        self.map[50][22].blocked = True
        self.map[50][22].block_sight = True

    def draw(self):
        #go through all tiles, and set their background color
        for y in range(self.height):
            for x in range(self.width):
                wall = self.map[x][y].block_sight
                if wall:
                    libtcod.console_put_char_ex(self.console, x, y, 2242, C.COLOR_DARK_WALL, C.COLOR_BACKGROUND_TEST)
                else:
                    libtcod.console_put_char_ex(self.console, x, y, 2242, C.COLOR_DARK_GROUND, C.COLOR_BACKGROUND)

    def get_starting_coords(self):
        return [ self.starting_coords['x'], self.starting_coords['y'] ]

    def create_room(self, room):
        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.map[x][y].blocked = False
                self.map[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        #horizontal tunnel. min() and max() are used in case x1>x2
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map[x][y].blocked = False
            self.map[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        #vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map[x][y].blocked = False
            self.map[x][y].block_sight = False

    def create_test_map(self):
        #create two rooms
        room1 = Rect(20, 15, 10, 15)
        room2 = Rect(50, 15, 10, 15)
        self.create_room(room1)
        self.create_room(room2)

        #connect them with a tunnel
        self.create_h_tunnel(25, 55, 23)
