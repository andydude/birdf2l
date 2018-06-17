import json
import sys
from argparse import ArgumentParser
from .speed import speed
from .posid import posid
from .generators import generators
from .parallel import metrics
from .models.pos import Pos


ID = {}
ALPHA = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_f2l_type(alg):
    try:
        state = Pos.from_alg(alg)
    except:
        return ""
    if state.is_ll():
        name = ""
    elif state.is_f2l_u():
        name = "U"
    elif state.is_f2l():
        name = "V"
    elif state.is_f2l_w():
        name = "W"
    elif state.is_f2l_x():
        name = "X"
    elif state.is_f2l_uv():
        name = "UV"
    elif state.is_f2l_vw():
        name = "VW"
    elif state.is_f2l_wx():
        name = "WX"
    elif state.is_f2l_xu():
        name = "XU"
    elif state.is_f2l_uw():
        name = "UW"
    elif state.is_f2l_vx():
        name = "VX"
    else:
        name = "?"
    return name


def algid(nmoves, alg=''):
    name = "!"
    if alg:
        name = get_f2l_type(alg)
    if not nmoves in ID:
        ID[nmoves] = 0
    ID[nmoves] += 1
    return '{}{}{}'.format(
        ALPHA[nmoves], name, 
        ID[nmoves])


def ollid1(up):
    assert len(up) == 8
    up = ''.join(sorted(list(up)))
    up = '{}{}{}{}{}{}{}{}'.format(
        up[0], up[4],
        up[1], up[5],
        up[2], up[6],
        up[3], up[7])
    return up


def ollid(posid):
    parts = posid.split('/')
    if len(parts) == 2:
        up, slot = parts
        if len(slot) == 2:
            up = ollid1(up)
            return '/'.join([up, slot])
        else:
            up = ollid1(up)
            slot = ollid1(slot)
            return '/'.join([up, slot])
    else:
        return ollid1(parts[0])


def patid(posid):
    parts = posid.split('/')
    if len(parts) == 2:
        if len(parts[1]) == 2:
            return parts[1]
        elif len(parts[1]) == 8:
            return parts[1][2:4]
    else:
        return "Vj"

    
def annotate(alg, algid='', names=''):
    gens = generators(alg) or ''
    pos = posid(alg)
    pat = patid(pos)[-2:]
    oll = ollid(pos)
    htm, qtm, stm = metrics(alg)
    return {
        'alg': alg,
        'algid': algid,
        'names': names,
        'ollid': oll,
        'patid': pat,
        'posid': pos,
        'gen': len(gens),
        'gens': gens,
        'speed': speed(alg),
        'htm': htm,
        'qtm': qtm,
        'stm': stm,
    }


def format_notes(notes):
    parts = notes.split(' ')
    parts = filter(lambda x: x, parts)
    parts = list(sorted(list(set(parts))))
    return ' '.join(parts)


def format_annotation(**kwargs):
    return ','.join([
        '', # id
        str(kwargs['speed']),
        str(kwargs['stm']),
        str(kwargs['htm']),
        str(kwargs['qtm']),
        str(kwargs['algid']),
        str(kwargs['ollid']),
        str(kwargs['posid']),
        str(kwargs['patid']),
        str(kwargs['alg']),
        format_notes(str(kwargs['gens']) + ' ' +
                     str(kwargs['names']))])


def add_arguments(parser):
    parser.add_argument('--csv', action='store_true')
    parser.add_argument('--json', action='store_true')
    return parser


def main():
    parser = add_arguments(ArgumentParser())
    options = vars(parser.parse_args(sys.argv[1:]))
    if options.get('csv', False):
        print("row,speed,stm,htm,qtm,algid,ollid,posid,patid,alg,notes")
    lines = sys.stdin.read()
    for line in lines.split('\n'):
        if line.startswith('htm'):
            continue
        if not line.strip():
            continue
        parts = line.split(',')
        try:
            if len(parts) == 0:
                raise ValueError
            elif len(parts) == 1:

                # 1 column means: alg
                alg = parts[0]
                names = ''
            else:
                
                # 2+ columns mean: alg, names
                alg = parts[-2]
                names = parts[-1]
                
            htm = alg.count(' ') + 1
            ann = annotate(alg, algid(htm, alg), names)
            if options.get('csv', False):
                print(format_annotation(**ann))
            else:
                print(json.dumps(ann, default=str, indent=4, sort_keys=True))
        except Exception as exc:
            print("# " + repr(exc))
            raise
            print(line)


if __name__ == '__main__':
    main()
