from .parallel import is_alt, is_opp

BONUS_U = 0.2
BONUS_ALT = 0.4  # Alternating bonus (R U R' U')
BONUS_PAR = 0.2  # Parallel bonus (L R')
PENALTY_D = 0.2
PENALTY_2 = 0.5


def speed(alg):
    moves = alg.split(' ')
    speed = [1 for _ in moves]
    for i, move in enumerate(moves):
        if 'U' in move:
            speed[i] = (1.0 - BONUS_U)
        if 'D' in move:
            speed[i] = (1.0 + PENALTY_D)
        if '2' in move:
            speed[i] *= (1.0 + PENALTY_2)
        if i >= 2 and is_alt(move, moves[i - 2]):
            speed[i] *= (1.0 - BONUS_ALT)
        if i >= 1 and is_opp(move, moves[i - 1]):
            speed[i] *= (1.0 - BONUS_PAR)
    return round(sum(speed), 2)
