ID = {}
ALPHA = "_ABCDEFGHIJKLMNOPQRSTUVWX"

def is_alt(side, side2):
    side, side2 = side[0], side2[0]
    return side == side2

def is_opp(side, side2):
    side, side2 = side[0], side2[0]
    if ord(side) > ord(side2):
        side, side2 = side2, side
    if side == 'D' and side2 == 'U':
        return True
    elif side == 'L' and side2 == 'R':
        return True
    elif side == 'B' and side2 == 'F':
        return True
    else:
        return False

def speed(alg):
    moves = alg.split(' ')
    speed = [1 for _ in moves]
    for i, move in enumerate(moves):
        if 'U' in move:
            speed[i] = 0.8
        if 'D' in move:
            speed[i] = 1.2
        if '2' in move:
            speed[i] *= 1.5
        if i >= 2 and is_alt(move, moves[i - 2]):
            speed[i] *= 0.6
        if i >= 1 and is_opp(move, moves[i - 1]):
            speed[i] *= 0.8
    return round(sum(speed), 2)

def name(nmoves):
    if not nmoves in ID:
        ID[nmoves] = 0
    ID[nmoves] += 1
    return 'V-{}{}'.format(
        ALPHA[nmoves], ID[nmoves])
    
if __name__ == '__main__':
    import sys
    
    #alg = sys.stdin.read()
    #print(speed(alg))
    lines = sys.stdin.read()
    for line in lines.split('\n'):
        try:
            parts = line.split(',')
            nmoves = int(parts[2])
            alg = parts[5]
            if not alg:
                raise ValueError
            if 'speed' in parts[1]:
                raise ValueError
            parts[3] = str(name(nmoves))
            parts[1] = str(speed(alg))
            print(','.join(parts))
        except:
            print(line)


