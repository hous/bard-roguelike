import libtcodpy as libtcod
import Constants as C

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
        self.map = [[ Tile(False)
            for y in range(self.height) ]
                for x in range(self.width) ]

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
                    libtcod.console_set_char_background(self.console, x, y, C.COLOR_DARK_WALL, libtcod.BKGND_SET )
                else:
                    libtcod.console_set_char_background(self.console, x, y, C.COLOR_DARK_GROUND, libtcod.BKGND_SET )
