import json
import sys
from argparse import ArgumentParser
from pandas import read_csv, DataFrame
from .generators import generators
from .models.alg import Alg
from .models.pos import Pos
from .parallel import metrics, htm4id
from .plugins import f2la
from .posid import posid
from .speed import speed

# TODO: port to birdf2l
from cubecode.canon import canonicalize1


#ALG = read_csv("fixtures/alg.csv", dtype=str, keep_default_na=False)
PAT = read_csv("fixtures/pat.csv", dtype=str, keep_default_na=False)
PAT_D = list(PAT.transpose().to_dict().values())
PAT_IDS = [pat['patid'] for pat in PAT_D]

ID = {}
ALPHA = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????"
MIRROR = True

def get_f2l_type(alg, pos=None):
    if not pos:
        pos = Pos.from_alg(alg)
    name = ""
    if not f2la.has_u_slot(pos):
        name += "U"
    if not f2la.has_v_slot(pos):
        name += "V"
    if not f2la.has_w_slot(pos):
        name += "W"
    if not f2la.has_x_slot(pos):
        name += "X"
    return name


def algid(nmoves, alg='', isoob=False):
    name = "!"
    if not alg:
        return
    if not nmoves in ID:
        ID[nmoves] = 0
    ID[nmoves] += 1
    name = get_f2l_type(alg)
    if isoob:
        if name == 'VW':
            alg2 = canonicalize1("y' " + alg + " y")
            print_oob_alg(nmoves, 'UV', alg2)

            if MIRROR:
                miralg = str(Alg(alg).mirror_f2l())
                print_oob_alg(nmoves, 'UV', miralg)
                miralg2 = canonicalize1("y " + miralg + " y'")
                print_oob_alg(nmoves, 'VW', miralg2)
        elif name == 'VWX':
            alg2 = canonicalize1("y' " + alg + " y")
            print_oob_alg(nmoves, 'UVW', alg2)
            alg3 = canonicalize1("y2 " + alg + " y2")
            print_oob_alg(nmoves, 'UVX', alg3)

            if MIRROR:
                miralg = str(Alg(alg).mirror_f2l())
                print_oob_alg(nmoves, 'UVX', miralg)
                miralg2 = canonicalize1("y " + miralg + " y'")
                print_oob_alg(nmoves, 'UVW', miralg2)
                miralg3 = canonicalize1("y2 " + miralg + " y2")
                print_oob_alg(nmoves, 'VWX', miralg3)
    return '{}{}{}'.format(
        ALPHA[nmoves], name,
        ID[nmoves])


def rotate_line(line, id=None, ann=None, isoob=False):
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

        ann0 = ann
        alg0 = alg
        if alg0.startswith("U"):
            alg0 = alg0[alg0.index(" ") + 1:]
        for us in ['', "U ", "U2 ", "U' "]:
            alg = us + alg0
            id = id if id else algid(htm4id(alg), alg)
            ann = annotate(alg, id, names)
            if ann['patid'] in PAT_IDS:
                print(format_annotation(**ann))
                break
        else:
            print("# could not find F2L pattern match for alg " + alg)
    except Exception as exc:
        print("# " + repr(exc))
        raise

        
def print_oob_alg(nmoves, name, alg=''):
    id = '{}{}{}'.format(
        ALPHA[nmoves], name,
        ID[nmoves])
    rotate_line(alg, id, isoob=True)

    
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
    parser.add_argument('--oob', action='store_true')
    parser.add_argument('--csv', action='store_true')
    parser.add_argument('--json', action='store_true')
    return parser


def main():
    parser = add_arguments(ArgumentParser())
    options = vars(parser.parse_args(sys.argv[1:]))
    iscsv = options.get('csv', False)
    isoob = options.get('oob', False)
    if iscsv:
        print("show,speed,stm,htm,qtm,algid,ollid,posid,patid,alg,notes")
        
    #for line in sys.stdin:
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        if line.startswith('htm'):
            continue
        if not line.strip():
            continue
        line = line.strip()
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
            if alg and alg[0].islower():
                continue

            id = algid(htm4id(alg), alg, isoob)
            ann = annotate(alg, id, names)
            if iscsv:
                print(format_annotation(**ann))
            else:
                print(json.dumps(ann, default=str, indent=4, sort_keys=True))
        except Exception as exc:
            print("# " + repr(exc))
            raise


if __name__ == '__main__':
    main()
