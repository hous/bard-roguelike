import libtcodpy as libtcod

# Console
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# Colors
COLOR_DARK_WALL = libtcod.Color(0, 0, 100)
COLOR_LIGHT_WALL = libtcod.Color(130, 110, 50)
COLOR_DARK_GROUND = libtcod.Color(50, 50, 150)
COLOR_LIGHT_GROUND = libtcod.Color(200, 180, 50)

COLOR_BACKGROUND = libtcod.black
COLOR_BACKGROUND_TEST = libtcod.yellow

# Dungeon Generator
DUNGEON_ROOM_MAX_SIZE = 10
DUNGEON_ROOM_MIN_SIZE = 6
DUNGEON_MAX_ROOMS = 30

# Field of View
FOV_ALGORITHM = 0
FOV_LIGHT_WALLS = True
