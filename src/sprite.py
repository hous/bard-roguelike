import libtcodpy as libtcod

class Sprite:
    #this is a generic game object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, console, x, y, char, color, blocks=True):
        self.console = console
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.blocks = blocks

    def move(self, dx, dy):
        #move by the given amount
        self.x += dx
        self.y += dy

    def draw(self):
        #set the color and then draw the character that represents this object at its position
        libtcod.console_set_default_foreground(self.console, self.color)
        libtcod.console_put_char(self.console, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(self.console, self.x, self.y, ' ', libtcod.BKGND_NONE)

    def collide(self, position):
        print "Collision at ", position