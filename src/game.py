fov_recompute = False
sprites = []
mobs = []
console = None
m = None
levels = []
current_level = 0
audio = None


def register_console(con):
    global console
    console = console


def register_audio(aud):
    global audio
    audio = aud


def register_sprite(sprite, player=False, mob=False):
    global player_one, sprites
    for s in sprites:
        if s is sprite: return
    if player:
        player_one = sprite
    if mob:
        mobs.append(sprite)
    sprites.append(sprite)


def register_map(new_map):
    global m
    m = new_map


def update_level(new_level):
    global current_level
    current_level = new_level


def update_mobs():
    global mobs
    for mob in mobs:
        mob.take_action()