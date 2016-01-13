fov_recompute = False
sprites = []
console = None
m = None


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
