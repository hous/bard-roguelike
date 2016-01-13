fov_recompute = False
sprites = []
console = None
m = None
levels = []
current_level = 0


def register_console(con):
    global console
    console = console


def register_sprite(sprite, player=False):
    global player_one, sprites
    for s in sprites:
        if s is sprite: return
    if player:
        player_one = sprite
    sprites.append(sprite)


def register_map(new_map):
    global m
    m = new_map


def update_level(new_level):
    global current_level
    current_level = new_level


