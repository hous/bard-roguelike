import libtcodpy as libtcod
import pprint

# DEBUG
DEBUG = False

# Console
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# Colors
COLOR_DARK_WALL = libtcod.Color(0, 0, 100)
COLOR_LIGHT_WALL = libtcod.Color(130, 110, 50)
COLOR_DARK_GROUND = libtcod.Color(50, 50, 150)
COLOR_LIGHT_GROUND = libtcod.Color(200, 180, 50)
COLOR_BACKGROUND = libtcod.black

# Characters
CHAR_DARK_WALL = 2242
CHAR_LIGHT_WALL = 2242
CHAR_DARK_GROUND = 2242
CHAR_LIGHT_GROUND = 2242

# Dungeon Generator
DUNGEON_ROOM_MAX_SIZE = 16
DUNGEON_ROOM_MIN_SIZE = 5
DUNGEON_MAX_ROOMS = 20

# Field of View
FOV_ALGORITHM = libtcod.FOV_SHADOW
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 4

# Mobs
PLAYER_ONE = dict(
    char="@",
    color=libtcod.white,
    description="This is you."
)

MOBS = dict(
    goblin=dict(
        char="g",
        color=libtcod.darker_green,
        name="goblin",
        description="A stinking, wretched little goblin."
    ),
    feral_cat=dict(
        char="c",
        color=libtcod.grey,
        name="feral cat",
        description="This cat looks skittish and hungry."
    )
)

