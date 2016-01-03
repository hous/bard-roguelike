#!/usr/bin/python
import sys, os

sys.path.append(os.path.abspath("./lib"))
sys.path.append(os.path.abspath("./classes"))

import libtcodpy as libtcod
import Constants as C
import Object as O
import Map as M

def handle_keys():
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

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)

def render_all():
    m.draw()

    #draw all objects in the list
    for object in objects:
        object.draw()

    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, C.SCREEN_WIDTH, C.SCREEN_HEIGHT, 0, 0, 0)

#############################################
# Initialization & Main Loop
#############################################

libtcod.console_set_custom_font('assets/fonts/font.png', libtcod.FONT_LAYOUT_ASCII_INROW | libtcod.FONT_TYPE_GREYSCALE, 32, 2048)
libtcod.console_init_root(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, 'python/libtcod tutorial', False)
con = libtcod.console_new(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)

m = M.Map(con, 80, 45)
m.create_test_map()
player_x, player_y = m.get_starting_coords()

player = O.Object(con, player_x, player_y, 1217, libtcod.white)
npc = O.Object(con, C.SCREEN_WIDTH/2 - 5, C.SCREEN_HEIGHT/2, 1218, libtcod.yellow)
objects = [npc, player]

while not libtcod.console_is_window_closed():

    render_all()

    libtcod.console_flush()

    #erase all objects at their old locations, before they move
    for object in objects:
        object.clear()

    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break
