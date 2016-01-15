#!/usr/bin/python
import sys, os

sys.path.append(os.path.abspath("./lib"))
sys.path.append(os.path.abspath("./src"))

import libtcodpy as libtcod
import constants as C
import game
from sprite import Sprite, Mob
from map import Map

#############################################
# libtcod Initialization & Main Loop
#############################################

def init():
    # libtcod.console_set_custom_font('assets/fonts/font.png', libtcod.FONT_LAYOUT_ASCII_INROW | libtcod.FONT_TYPE_GREYSCALE, 32, 2048)
    libtcod.console_set_custom_font('assets/fonts/dejavu16x16_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    game.register_console(libtcod.console_new(C.SCREEN_WIDTH, C.SCREEN_HEIGHT))

    game.register_map(Map(game.console, 80, 45))
    player_one_coords = game.m.get_starting_coords()

    # Ready Player One
    game.register_sprite(Mob(game.console, C.PLAYER_ONE, player_one_coords), True)
    game.m.register_protagonist(game.player_one)

    # Test Mobs
    game.register_sprite(Mob(game.console, C.MOBS["goblin"], (player_one_coords[0] + 1, player_one_coords[1])))
    game.register_sprite(Mob(game.console, C.MOBS["feral_cat"], (player_one_coords[0] - 1, player_one_coords[1])))

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
        exit = handle_keys()
        if exit:
            break


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
        return True

    # movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        try_move(game.player_one, (0, -1))
        game.fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        try_move(game.player_one, (0, 1))
        game.fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        try_move(game.player_one, (-1, 0))
        game.fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        try_move(game.player_one, (1, 0))
        game.fov_recompute = True


def try_move(sprite, direction):
    if game.m.is_blocked(game.player_one.coords[0] + direction[0], game.player_one.coords[1] + direction[1]):
        sprite.collide((direction[0], direction[1]))
    else:
        sprite.move(direction[0], direction[1])

# Get after it
init()