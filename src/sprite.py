import libtcodpy as libtcod
import dice
import math

class Sprite(object):
    # this is a generic game object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.
    def __init__(self, console, config, position, blocks=True, mob=None, ai=None):
        print config
        self.console = console
        self.name = config["name"]
        self.char = config["char"]
        self.color = config["color"]
        self.description = config["description"]
        self.position = position
        self.blocks = blocks

        # This is weird
        self.mob = mob
        if self.mob:
            self.mob.owner = self
        self.ai = ai
        if self.ai:
            self.ai.owner = self

    def move(self, dx, dy):
        # move by the given amount
        self.position[0] += dx
        self.position[1] += dy

    def draw(self):
        # set the color and then draw the character that represents this object at its position
        libtcod.console_set_default_foreground(self.console, self.color)
        libtcod.console_put_char(self.console, self.position[0], self.position[1], self.char, libtcod.BKGND_NONE)

    def clear(self):
        # erase the character that represents this object
        libtcod.console_put_char(self.console, self.position[0], self.position[1], ' ', libtcod.BKGND_NONE)

    def collide_wall(self, sprite, x, y):
        print "collision with", sprite, "and a wall at", (x, y)

    def collide_sprite(self, collider, collidee, x, y):
        print "collision with", collider, "and", collidee, "at", (x, y)


class Player(Sprite):
    def __init__(self, console, config, position):
        mob = Mob(config)
        super(Player, self).__init__(console=console, config=config, position=position, blocks=True)


class Mob():
    def __init__(self, config):
        self.max_hp = dice.roll(config["health"])
        self.current_hp = self.max_hp

    def attack(self, target):
        pass

class AI():
    def __init__(self, config):
        self.detection_range = config["detection_range"]

    def take_action(self, map, protagonist):
        if map.get_distance(self.owner.position, protagonist.position) <= self.detection_range:
            direction = self.get_direction(protagonist.position)
            new_position = [self.owner.position[0] + direction[0], self.owner.position[1] + direction[1]]

            # Pretty dumb AI at this point. Will get stuck on walls if the preferred direction blocks... need to fix @TODO
            if map.is_blocked(new_position[0], new_position[1]):
                self.owner.collide_wall(direction[0], direction[1])
            if new_position == protagonist.position:
                self.owner.collide_sprite(direction[0], direction[1])
            else:
                self.owner.move(direction[0], direction[1])

    def get_direction(self, target_position):
        dx = target_position[0] - self.owner.position[0]
        dy = target_position[1] - self.owner.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return [dx, dy]

    # Should be the "go after protagonist" part of the take_action
    def chase(self, target_position):
        pass