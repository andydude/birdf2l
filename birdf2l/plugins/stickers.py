import re
from birdf2l.models.pos import Pos


STICKERS_CTR = [
    {"is": ["Y"], "at": [( 1, 4)]},  # U
    {"is": ["W"], "at": [( 7, 4)]},  # D
    {"is": ["O"], "at": [( 4, 7)]},  # R
    {"is": ["R"], "at": [( 4, 1)]},  # L
    {"is": ["G"], "at": [( 4, 4)]},  # F
    {"is": ["B"], "at": [( 4,10)]},  # B
]

STICKERS_E = [
    {"is": ["Y", "B"], "at": [( 0, 4), ( 3,10)]},  # UB
    {"is": ["Y", "O"], "at": [( 1, 5), ( 3, 7)]},  # UR
    {"is": ["Y", "G"], "at": [( 2, 4), ( 3, 4)]},  # UF
    {"is": ["Y", "R"], "at": [( 1, 3), ( 3, 1)]},  # UL
    {"is": ["R", "G"], "at": [( 4, 2), ( 4, 3)]},  # LF
    {"is": ["G", "O"], "at": [( 4, 5), ( 4, 6)]},  # RF
    {"is": ["O", "B"], "at": [( 4, 8), ( 4, 9)]},  # RB
    {"is": ["B", "R"], "at": [( 4,11), ( 4, 0)]},  # LB
    {"is": ["W", "G"], "at": [( 6, 4), ( 5, 4)]},  # DF
    {"is": ["W", "O"], "at": [( 7, 5), ( 5, 7)]},  # DR
    {"is": ["W", "B"], "at": [( 8, 4), ( 5,10)]},  # DB
    {"is": ["W", "R"], "at": [( 7, 3), ( 5, 1)]},  # DL
]

STICKERS_C = [
    {"is": ["Y", "R", "B"], "at": [( 0, 3), ( 3, 0), ( 3,11)]},  # LUB
    {"is": ["Y", "B", "O"], "at": [( 0, 5), ( 3, 9), ( 3, 8)]},  # RUB
    {"is": ["Y", "O", "G"], "at": [( 2, 5), ( 3, 6), ( 3, 5)]},  # RUF
    {"is": ["Y", "G", "R"], "at": [( 2, 3), ( 3, 3), ( 3, 2)]},  # LUF
    {"is": ["W", "R", "G"], "at": [( 6, 3), ( 5, 2), ( 5, 3)]},  # LDF
    {"is": ["W", "G", "O"], "at": [( 6, 5), ( 5, 5), ( 5, 6)]},  # RDF
    {"is": ["W", "O", "B"], "at": [( 8, 5), ( 5, 8), ( 5, 9)]},  # RDB
    {"is": ["W", "B", "R"], "at": [( 8, 3), ( 5,11), ( 5, 0)]},  # LDB
]

STICKERS_RE = re.compile(r"[^\w]")


def unstickers(value):
    value = STICKERS_RE.sub('', value)
    return value


def decode(value):
    from pycuber import Cube
    from pycuber.helpers import array_to_cubies
    from .pycuber import _stickers2array
    #from .pycuber import encode as _encode
    from .pycuber import decode as _decode
    value = _stickers2array(value)
    cube = Cube(array_to_cubies(value))
    pos = _decode(cube)
    return pos

    #from .pycuber import decode as _decode
    #cube = _decode(value)
    #pos = _encode(cube)
    #return pos


def encode(pos):
    assert isinstance(pos, Pos)
    linesize = 12
    lines = [
        bytearray(
            ("{0:" + str(linesize) + "s}").format("").encode('latin1'))
        for _ in range(9)]
    for ctr in range(0, 6):
        d = STICKERS_CTR[ctr]
        p = STICKERS_CTR[pos.rp[ctr]]
        dis, dat = d['is'], p['at']
        for ix, _ in enumerate(dis):
            st, at = dis[ix], dat[ix]
            lines[at[0]][at[1]] = ord(st)
    for c in range(0, 8):
        d = STICKERS_C[c]
        p = STICKERS_C[pos.cp[c]]
        o = pos.co[c]
        dis, dat = d['is'], p['at']
        for ix, _ in enumerate(dis):
            st, at = dis[(ix + o) % 3], dat[ix]
            lines[at[0]][at[1]] = ord(st)
    for e in range(0, 12):
        d = STICKERS_E[e]
        p = STICKERS_E[pos.ep[e]]
        o = pos.eo[e]
        dis, dat = d['is'], p['at']
        for ix, _ in enumerate(dis):
            st, at = dis[(ix + o) % 2], dat[ix]
            lines[at[0]][at[1]] = ord(st)
    return '\n'.join([line.decode('latin1') for line in lines])
