protagonist = None
fov_recompute = False
sprites = []
ais = []
console = None
m = None
levels = []
current_level = 0
audio = None


def register_console(con):
    global console
    console = con


def register_audio(aud):
    global audio
    audio = aud


def register_sprite(sprite, player=False):
    global protagonist, sprites
    for s in sprites:
        if s is sprite: return
    if player:
        protagonist = sprite
    if sprite.ai:
        print "Found AI:", sprite.ai
        ais.append(sprite.ai)

    sprites.append(sprite)


def register_map(new_map):
    global m
    m = new_map


def update_level(new_level):
    global current_level
    current_level = new_level


def update_ais():
    global ais
    for ai in ais:
        # Give each AI a reference to the Map and Protagonist??
        ai.take_action(m, protagonist)


def get_sprite_at_position(x, y):
    global sprites
    for sprite in sprites:
        if sprite.position is (x, y):
            return sprite
    return None


def collide_wall(sprite, x, y):
    print "collision with", sprite, "and a wall at", (x, y)


def collide_sprite(collider, collidee, x, y):
    print "collision with", collider, "and", collidee, "at", (x, y)

