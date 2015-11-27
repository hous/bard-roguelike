#!/usr/bin/python
import sys, os

sys.path.append(os.path.abspath("./lib"))
sys.path.append(os.path.abspath("./classes"))

import libtcodpy as libtcod
import Constants as C
import Object as O
import Map as M

def handle_keys():
    global player_x, player_y

    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game

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

    m = M.Map(con, 80, 45)
    m.draw()

    #draw all objects in the list
    for object in objects:
        object.draw()

    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, C.SCREEN_WIDTH, C.SCREEN_HEIGHT, 0, 0, 0)

#############################################
# Initialization & Main Loop
#############################################

libtcod.console_set_custom_font('assets/fonts/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, 'python/libtcod tutorial', False)
con = libtcod.console_new(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)

player = O.Object(con, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2, '@', libtcod.white)
npc = O.Object(con, C.SCREEN_WIDTH/2 - 5, C.SCREEN_HEIGHT/2, '@', libtcod.yellow)
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
