#!/usr/bin/python
import sys, os

sys.path.append(os.path.abspath("./lib"))
sys.path.append(os.path.abspath("./src"))

import libtcodpy as libtcod
import constants as C
import game
from sprite import Mob, Player
from map import Map
from audio import Audio


#############################################
# libtcod Initialization & Main Loop
#############################################

def init():

    # libtcod.console_set_custom_font('assets/fonts/font.png', libtcod.FONT_LAYOUT_ASCII_INROW | libtcod.FONT_TYPE_GREYSCALE, 32, 2048)
    libtcod.console_set_custom_font('assets/fonts/dejavu16x16_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    game.register_console(libtcod.console_new(C.SCREEN_WIDTH, C.SCREEN_HEIGHT))

    game.register_audio(Audio())
    game.register_map(Map(game.console, 80, 45))
    player_one_position = game.m.get_starting_position()

    # Ready Player One
    game.register_sprite(Player(console=game.console, config=C.PLAYER_ONE, position=player_one_position), player=True)
    game.m.register_protagonist(game.protagonist)

    game.m.populate_rooms()

    while not libtcod.console_is_window_closed():
        game.m.draw()

        # draw all objects in the list
        for sprite in game.sprites:
            sprite.draw()

        # blit the contents of "con" to the root console
        libtcod.console_blit(game.console, 0, 0, C.SCREEN_WIDTH, C.SCREEN_HEIGHT, 0, 0, 0)

        libtcod.console_flush()

        # erase all objects at their old locations, before they move
        for sprite in game.sprites:
            sprite.clear()

        # handle keys and exit game if needed
        player_action = handle_keys()
        if player_action == 'exit':
            # kill sound and exit
            game.audio.kill()
            break

        if player_action != 'no-action':
            game.update_ais()

#############################################
# Input
#############################################


def handle_keys():
    game.fov_recompute = False

    key = libtcod.console_wait_for_keypress(True)

    # Alt+Enter: toggle fullscreen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    # Escape to exit game
    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'

    # movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        try_move(game.protagonist, (0, -1))
        game.fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        try_move(game.protagonist, (0, 1))
        game.fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        try_move(game.protagonist, (-1, 0))
        game.fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        try_move(game.protagonist, (1, 0))
        game.fov_recompute = True

    else:
        return 'no-action'


def try_move(sprite, direction):
    x, y = game.protagonist.position[0] + direction[0], game.protagonist.position[1] + direction[1]
    collidee = game.get_sprite_at_position(x, y)

    if game.m.is_blocked(x, y):
#        game.audio.play_sound()
        game.collide_wall(sprite, direction[0], direction[1])

    if collidee is not None:
        game.collide_sprite(sprite, collidee)

    else:
        sprite.move(direction[0], direction[1])

# Get after it
init()