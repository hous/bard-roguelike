import libtcodpy as libtcod
import constants as C
import dice
from shape import Rect, Circle
from sprite import Sprite, Mob
import game


class Tile(object):
    # An individual tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        # All tiles are unexplored by default
        self.explored = False

        # By default, if a tile is blocked, it also blocks sight. May need to change for glass / ice?
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight


class Map(object):
    def __init__(self, console, width, height, config = None):
        self.console = console
        self.width = width
        self.height = height
        self.config = config
        self.rooms = []
        self.protagonist = None
        self.starting_coords = {'x': 0, 'y': 0}
        self.map = [[Tile(True)
                    for y in range(self.height)]
                    for x in range(self.width)]
        self.generate_map()
        self.fov_map = None
        self.generate_fov_map()

    def register_protagonist(self, sprite):
        # Get a reference to the sprite that will be determining field-of-view
        self.protagonist = sprite

    def generate_map(self):
        for count in range(C.DUNGEON_MAX_ROOMS):
            num_rooms = len(self.rooms)
            # 1/5 of rooms as circles
            if libtcod.random_get_int(0, 0, 5) == 4:
                r = libtcod.random_get_int(0, C.DUNGEON_ROOM_MIN_SIZE, C.DUNGEON_ROOM_MAX_SIZE / 2)
                x = libtcod.random_get_int(0, r, self.width - r - 2)
                y = libtcod.random_get_int(0, r, self.height - r - 2)
                new_room = Circle(x, y, r)
            else:
                w = libtcod.random_get_int(0, C.DUNGEON_ROOM_MIN_SIZE, C.DUNGEON_ROOM_MAX_SIZE)
                h = libtcod.random_get_int(0, C.DUNGEON_ROOM_MIN_SIZE, C.DUNGEON_ROOM_MAX_SIZE)
                x = libtcod.random_get_int(0, 1, self.width - w - 2)
                y = libtcod.random_get_int(0, 1, self.height - h - 2)
                new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                # this means there are no intersections, so this room is valid
                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                # Display Room names for debugging
                if C.DEBUG:
                    debug_sprite_config = dict(
                        char=chr(65+num_rooms),
                        color=libtcod.white,
                        description="A debugging character."
                    )
                    room_no = Sprite(game.console, debug_sprite_config, (new_x, new_y), False)
                    game.sprites.insert(0, room_no)

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    self.starting_coords['x'] = new_x
                    self.starting_coords['y'] = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = self.rooms[num_rooms-1].center()

                    # draw a coin (random number that is either 0 or 1)
                    if libtcod.random_get_int(0, 0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                self.rooms.append(new_room)
                num_rooms += 1

    def generate_fov_map(self):
        self.fov_map = libtcod.map_new(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                libtcod.map_set_properties(self.fov_map, x, y, not self.map[x][y].block_sight, not self.map[x][y].blocked)

    def draw(self):
        if game.fov_recompute:
            # recompute FOV if needed (the player moved or something)
            game.fov_recompute = False
            # yuck, shouldn't need to reference
            libtcod.map_compute_fov(self.fov_map, self.protagonist.coords[0], self.protagonist.coords[1], C.TORCH_RADIUS, C.FOV_LIGHT_WALLS, C.FOV_ALGORITHM)

        # go through all tiles, and set their background color according to the FOV
        for y in range(self.height):
            for x in range(self.width):
                visible = libtcod.map_is_in_fov(self.fov_map, x, y) if not C.DEBUG else True
                wall = self.map[x][y].block_sight
                if not visible:
                    # if it's not visible right now, the player can only see it if it's explored
                    if self.map[x][y].explored:
                        if wall:
                            libtcod.console_set_char_background(self.console, x, y, C.COLOR_DARK_WALL, libtcod.BKGND_SET)
                            # libtcod.console_put_char_ex(self.console, x, y, 2242, C.COLOR_DARK_WALL, C.COLOR_BACKGROUND)
                        else:
                            libtcod.console_set_char_background(self.console, x, y, C.COLOR_DARK_GROUND, libtcod.BKGND_SET)
                            # libtcod.console_put_char_ex(self.console, x, y, 2242, C.COLOR_DARK_GROUND, C.COLOR_BACKGROUND)
                else:
                    # it's visible
                    if wall:
                        libtcod.console_set_char_background(self.console, x, y, C.COLOR_LIGHT_WALL, libtcod.BKGND_SET)
                        # libtcod.console_put_char_ex(self.console, x, y, 2242, C.COLOR_LIGHT_WALL, C.COLOR_BACKGROUND)
                    else:
                        libtcod.console_set_char_background(self.console, x, y, C.COLOR_LIGHT_GROUND, libtcod.BKGND_SET)
                        # libtcod.console_put_char_ex(self.console, x, y, 2242, C.COLOR_LIGHT_GROUND, C.COLOR_BACKGROUND)

                    # since it's visible, explore it
                    self.map[x][y].explored = True

    def is_blocked_deprecated(self, x, y):
        print self.is_blocked_functional(x, y)
        # first test the map tiles
        if self.map[x][y].blocked:
            return True

        # now check for any blocking objects
        for sprite in game.sprites:
            if sprite.blocks and sprite.coords[0] == x and sprite.coords[1] == y:
                print sprite.coords
                return True

        return False

    def is_blocked(self, x, y):
        # Trying out some functional programming. Would need to pass in sprites and map in order to really be functional though
        return self.map[x][y].blocked or any(map(lambda sprite: sprite.coords == (x, y), game.sprites))

    def get_starting_coords(self):
        return [self.starting_coords['x'], self.starting_coords['y']]

    def create_room(self, room):
        # go through the tiles in the room and make them passable
        for i in room.area():
            self.map[i[0]][i[1]].blocked = False
            self.map[i[0]][i[1]].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        # horizontal tunnel. min() and max() are used in case x1>x2
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map[x][y].blocked = False
            self.map[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        # vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map[x][y].blocked = False
            self.map[x][y].block_sight = False

    # This doesn't belong here.
    def populate_rooms(self):
        for room in self.rooms:
            mob_count = libtcod.random_get_int(0, 0, C.DUNGEON_MAX_MOBS_PER_ROOM)
            for i in range(mob_count):
                room_area = room.area()
                coordinate = room_area[libtcod.random_get_int(0, 0, len(room_area) - 1)]
                x, y = coordinate[0], coordinate[1]
                if not self.is_blocked(x, y):
                    game.register_sprite(Mob(game.console, C.MOBS["goblin"], (x, y)), mob=True)

    def get_distance(self, coordinate_one, coordinate_two):
        pass