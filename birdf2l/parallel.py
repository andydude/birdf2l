def is_alt(side, side2):
    side, side2 = side[0], side2[0]
    return side == side2


def is_opp(side, side2):
    side, side2 = side[0], side2[0]
    if ord(side) > ord(side2):
        side, side2 = side2, side
    if side == 'D' and side2 == 'U':
        return True
    elif side == 'D' and side2 == 'y':
        return True
    elif side == 'U' and side2 == 'y':
        return True
    elif side == 'L' and side2 == 'R':
        return True
    elif side == 'L' and side2 == 'x':
        return True
    elif side == 'R' and side2 == 'x':
        return True
    elif side == 'B' and side2 == 'F':
        return True
    elif side == 'B' and side2 == 'z':
        return True
    elif side == 'F' and side2 == 'z':
        return True
    else:
        return False

    
def get_angle(move):
    if not move:
        return 0
    elif move.endswith("'"):
        return -1
    elif move.endswith("2"):
        return 2
    else:
        return 1

    
def stm1(side, side2):
    if ord(side[0]) > ord(side2[0]):
        side, side2 = side2, side
    angle, angle2 = get_angle(side), get_angle(side2)
    if is_opp(side, side2):
        if (angle + angle2) == 0:
            return (2, 1)
        else:
            return (2, 2)
    else:
        return (1, 1)

    
def stm(alg):
    skip = False
    m = 0
    moves = alg.split(' ')
    if len(moves) == 1:
        return 1
    for i, move in enumerate(moves):
        if skip:
            skip = False
            continue
        nmoves, metric = stm1(move, moves[i - 1])
        m += metric
        if nmoves == 2:
            skip = True
            continue
        skip = False
    return m


def qtm1(alg):
    if '2' in alg:
        return 2
    else:
        return 1

    
def qtm(alg):
    moves = alg.split(' ')
    return sum([qtm1(move) for move in moves])


def metrics(alg):
    htm = alg.count(' ') + 1
    return htm, qtm(alg), stm(alg)

