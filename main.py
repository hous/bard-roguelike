#!/usr/bin/python
import sys, os

sys.path.append(os.path.abspath("./lib"))
sys.path.append(os.path.abspath("./src"))

import libtcodpy as libtcod
import Constants as C
import Game
from Sprite import Sprite
from Map import Map

#############################################
# libtcod Initialization & Main Loop
#############################################

def init():
    libtcod.console_set_custom_font('assets/fonts/font.png', libtcod.FONT_LAYOUT_ASCII_INROW | libtcod.FONT_TYPE_GREYSCALE, 32, 2048)
    libtcod.console_init_root(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    con = libtcod.console_new(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)

    m = Map(con, 80, 45)
    m.create_test_map()
    player_x, player_y = m.get_starting_coords()

    player = Sprite(con, player_x, player_y, 1217, libtcod.white)
    npc = Sprite(con, C.SCREEN_WIDTH/2 - 5, C.SCREEN_HEIGHT/2, 1218, libtcod.yellow)
    objects = [npc, player]

    while not libtcod.console_is_window_closed():
        m.draw()

        #draw all objects in the list
        for object in objects:
            object.draw()

        #blit the contents of "con" to the root console
        libtcod.console_blit(con, 0, 0, C.SCREEN_WIDTH, C.SCREEN_HEIGHT, 0, 0, 0)

        libtcod.console_flush()

        #erase all objects at their old locations, before they move
        for object in objects:
            object.clear()

        #handle keys and exit game if needed
        exit = handle_keys()
        if exit:
            break

#############################################
# Input
#############################################

def handle_keys():
    Game.fov_recompute = False

    key = libtcod.console_wait_for_keypress(True)

    #Alt+Enter: toggle fullscreen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    #Escape to exit game
    elif key.vk == libtcod.KEY_ESCAPE:
        return True

    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1)
        Game.fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)
        Game.fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)
        Game.fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)
        Game.fov_recompute = True

init()