import random
import roll_vals


def roll(n, max, mode='reg'):
    n = int(n)
    max = int(max)
    success = 0

    if mode == 'reg':
        for i in range(n):
            roll_vals.d_roll = random.randint(1, max)
            roll_vals.rolls.append(roll_vals.d_roll)
            roll_vals.total += roll_vals.d_roll

    elif mode == "ex":
        for i in range(n):
            roll_vals.d_roll = random.randint(1, max)
            roll_vals.rolls.append(roll_vals.d_roll)
            roll_vals.total += roll_vals.d_roll

            if roll_vals.d_roll == max:
                roll_vals.d_roll = random.randint(1, max)
                roll_vals.extra_rolls.append(roll_vals.d_roll)
                roll_vals.total += roll_vals.d_roll

    elif mode == "exc":
        for i in range(n):
            roll_vals.d_roll = random.randint(1, max)
            roll_vals.rolls.append(roll_vals.d_roll)
            roll_vals.total += roll_vals.d_roll

            if roll_vals.d_roll == max:
                explode(max)
    else:
        return "Sorry, but you've entered an incorrect mode"

    for i in roll_vals.rolls:
        if i > (max // 2):
            success += 1

        #Returning all the values
    return f"""You rolled: {roll_vals.rolls}
{extra_check()}
Total: {roll_vals.total}
{success} successes!"""


def explode(max):
    roll_vals.d_roll = random.randint(1, max)
    roll_vals.extra_rolls.append(roll_vals.d_roll)
    roll_vals.total += roll_vals.d_roll

    if roll_vals.d_roll == max:
        explode(max)


def reset_vals():
    roll_vals.d_roll = 0
    roll_vals.rolls = []
    roll_vals.total = 0
    roll_vals.extra_rolls = []


def extra_check():
    if roll_vals.extra_rolls:
        return f'Extra die: {roll_vals.extra_rolls}'
    else:
        return '(No extra dice)'


def main(string):  #input cleaning and checking
    reset_vals()
    if string.startswith('exc'):
        string = string.replace('exc', '').split('d')
        return roll(string[0], string[1], 'exc')
    elif string.startswith('ex'):
        string = string.replace('ex', '').split('d')
        return roll(string[0], string[1], 'ex')
    else:
        string = string.split('d')
        return roll(string[0], string[1], 'reg')
