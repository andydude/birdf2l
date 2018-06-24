from birdf2l.models.alg import Alg
from birdf2l.models.pos import Pos
import json
import sys

OPP_FACES = {
    "R": "L",
    "U": "D",
    "F": "B",
}
"""
def htm(alg):
    '''
    This assumes that LL algs never start with U.
    '''
    m = alg.count(' ')
    m += 0 if alg[0] == 'U' else 1
    return m

| name?\a0=U? | False | True  |
| ----------- | ----- | ----- |
|       False |   1   |   1   |
|       True  |   1   |   0   |
"""
def iterstep(faces, previous_face, parallel=False):
    for face in faces:
        if previous_face != face:
            if parallel:
                opp_face = OPP_FACES[face]
                yield "{}".format(face)
                yield "{}'".format(face)
                yield "{}2".format(face)
                yield "{}".format(opp_face)
                yield "{}'".format(opp_face)
                yield "{}2".format(opp_face)
                yield "{} {}".format(opp_face, face)
                yield "{} {}'".format(opp_face, face)
                yield "{}' {}".format(opp_face, face)
                yield "{}' {}'".format(opp_face, face)
                yield "{} {}2".format(opp_face, face)
                yield "{}' {}2".format(opp_face, face)
                yield "{}2 {}".format(opp_face, face)
                yield "{}2 {}'".format(opp_face, face)
                #yield "{}2 {}2".format(opp_face, face)
            else:
                yield face
                yield face + "2"
                yield face + "'"

            
def iteralgs(faces, previous_face, depth, parallel=False):
    if depth == 0:
        return
    elif depth == 1:
        for alg in iterstep(faces, previous_face, parallel):
            yield alg
    else:
        for alg_first in iterstep(faces, previous_face, parallel):
            previous_face0 = alg_first[0]
            if previous_face0 in OPP_FACES.values():
                for k, v in OPP_FACES.items():
                    if v == previous_face0:
                        previous_face0 = k
            for alg_rest in iteralgs(faces, previous_face0, depth - 1, parallel):
                alg = alg_first + ' ' + alg_rest
                yield alg


FACES = list("RUF")
ALPHA = "_ABCDEFGHIJKLMNOP"
N = int(sys.argv[1])

from birdf2l.annotate import get_f2l_type
from birdf2l.plugins import f2la

for alg in iteralgs(FACES, 'X', N, True):    
    state = Pos.from_alg(alg)
    if not f2la.has_cross(state):
        continue
    name = get_f2l_type(alg, state)
    if not name:
        continue
    if name not in ['V', 'VW', 'VX', 'VWX']:
        continue
    antialg = str(Alg(alg).inverse())
    if antialg.startswith("U"):
        continue
    length = alg.count(' ') + 1
    print("{},{}{}?,{},".format(
        length, ALPHA[length], name, alg))
