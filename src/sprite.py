import libtcodpy as libtcod


class Sprite:
    # this is a generic game object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.
    def __init__(self, console, coords, char, color, blocks=True):
        self.console = console
        self.coords = coords
        self.char = char
        self.color = color
        self.blocks = blocks

    def move(self, dx, dy):
        # move by the given amount
        self.coords[0] += dx
        self.coords[1] += dy

    def draw(self):
        # set the color and then draw the character that represents this object at its position
        libtcod.console_set_default_foreground(self.console, self.color)
        libtcod.console_put_char(self.console, self.coords[0], self.coords[1], self.char, libtcod.BKGND_NONE)

    def clear(self):
        # erase the character that represents this object
        libtcod.console_put_char(self.console, self.coords[0], self.coords[1], ' ', libtcod.BKGND_NONE)

    def collide(self, position):
        print "Collision at ", position


class Mob(Sprite):
    def __init__(self, console, coords, char, color, config):
        super(Mob, self).__init__(self, console, coords, char, color, True)
        self.config = config
