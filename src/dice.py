import libtcodpy as libtcod

def roll(dice):
    # Collapse an un-rolled dice descriptor into its value, e.g. "2d6" = 7
    # Dice descriptors can be of format XdY+Z where X, Y, and Z are integers and "d" is just the character "d"
    # Can also just be a number Z, e.g. 12

    dice_split = dice.split('d')
    die_count = int(dice_split[0])
    adder = 0
    print dice_split
    if len(dice_split) > 1:
        if dice_split[1].find('+') > 0:
            dice_split_again = dice_split[1].split('+')
            die_type = int(dice_split_again[0])
            adder = int(dice_split_again[1])
        elif dice_split[1].find('-') > 0:
            dice_split_again = dice_split[1].split('-')
            die_type = int(dice_split_again[0])
            adder = -1 * int(dice_split_again[1])
        else:
            die_type = int(dice_split[1])

    else:
        return int(dice)

    value = reduce(lambda x, y: x + libtcod.random_get_int(0, 1, die_type) + adder, range(1, die_count + 1))
    print value
    return value

def flip_coin():
    return libtcod.random_get_int(0, 0, 1)