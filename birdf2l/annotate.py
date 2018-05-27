import json
import sys
from argparse import ArgumentParser
from .speed import speed
from .posid import posid
from .generators import generators
from .parallel import metrics


ID = {}
ALPHA = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def algid(nmoves):
    if not nmoves in ID:
        ID[nmoves] = 0
    ID[nmoves] += 1
    return 'V-{}{}'.format(
        ALPHA[nmoves], ID[nmoves])


def annotate(alg, algid='', names=''):
    gens = generators(alg) or ''
    pos = posid(alg)
    pat = pos[-2:]
    htm, qtm, stm = metrics(alg)
    return {
        'alg': alg,
        'algid': algid,
        'names': names,
        'patid': pat,
        'posid': pos,
        'gen': len(gens),
        'gens': gens,
        'speed': speed(alg),
        'htm': htm,
        'qtm': qtm,
        'stm': stm,
    }


def format_annotation(**kwargs):
    return ','.join([
        '', # id
        str(kwargs['speed']),
        str(kwargs['stm']),
        str(kwargs['htm']),
        str(kwargs['qtm']),
        str(kwargs['algid']),
        str(kwargs['posid']),
        str(kwargs['patid']),
        str(kwargs['alg']),
        str(kwargs['gens']) + ' ' +
        str(kwargs['names'])])


def add_arguments(parser):
    parser.add_argument('--csv', action='store_true')
    parser.add_argument('--json', action='store_true')
    return parser


def main():
    parser = add_arguments(ArgumentParser())
    options = vars(parser.parse_args(sys.argv[1:]))
    if options.get('csv', False):
        print("row,speed,stm,htm,qtm,algid,posid,patid,alg,notes")
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
            ann = annotate(alg, algid(htm), names)
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
