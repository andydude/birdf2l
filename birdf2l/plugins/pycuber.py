from .stickers import unstickers
from birdf2l.models.pos import Pos

ESEQ = [
    #123456789ABC
    "ABCDFJNRUVWX",  # 0-orientation
    "QMIELPTHKOSG",  # 1-orientation
]

EMAP = {
    'BU': 'AQ',
    'RU': 'BM',
    'UF': 'CI',
    'UL': 'DE',
    'LF': 'FL',
    'RF': 'JP',
    'BR': 'NT',
    'BL': 'RH',
    'DF': 'UK',
    'RD': 'VO',
    'BD': 'WS',
    'LD': 'XG',
}

# This converts back to a specific orientation
INVEMAP = {  # Official
    'AQ': 'UB',
    'BM': 'UR',
    'CI': 'UF',
    'DE': 'UL',
    'FL': 'LF',
    'JP': 'FR',
    'NT': 'RB',
    'RH': 'BL',
    'UK': 'DF',
    'VO': 'DR',
    'WS': 'DB',
    'XG': 'DL',
}

CSEQ = [
    #12345678
    "ABCDUVWX",  # 0-orientation
    "EQMIGKOS",  # 1-orientation
    "RNJFLPTH",  # 2-orientation
]

# Map from standard to Speffz
CMAP = {
    'BUL': 'AER',  # = E, R, Bull
    'BRU': 'BQN',  # = N, Q, Brew
    'RUF': 'CMJ',  # = J, M, Fur
    'ULF': 'DIF',  # = F, I, Flu
    'FLD': 'UGL',  # = G, L, Field
    'RDF': 'VKP',  # = K, P, Friday
    'BRD': 'WOT',  # = O, T, Bird
    'BLD': 'XSH',  # = S, H, Blind
}

# For orientation calculation
INVCMAP = {
    'AER': 'ULB',
    'BQN': 'UBR',
    'CMJ': 'URF',
    'DIF': 'UFL',
    'UGL': 'DLF',
    'VKP': 'DFR',
    'WOT': 'DRB',
    'XSH': 'DBL',
}

ROTOLD = "UDRLFB"
ROTMAP = {
    'U': 'Y',
    'L': 'R',
    'F': 'G',
    'R': 'O',
    'B': 'B',
    'D': 'W',
}

INVROTMAP = dict([(v, k) for k, v in ROTMAP.items()])

SMAP = {  # stickers
    'B': 'blue',
    'G': 'green',
    'O': 'orange',
    'R': 'red',
    'W': 'white',
    'Y': 'yellow',
}
ESEQ
INVSMAP = dict([(v, k) for k, v in SMAP.items()])


def _center2state(piece):
    image = piece.location
    sticker = list(piece.facings.items())[0]
    preimage = INVROTMAP[INVSMAP[sticker[1].colour]]
    return (
        ROTOLD.index(preimage),
        ROTOLD.index(image))


def _edge2state(piece):
    image = piece.location
    preimage = ""
    for sticker in piece.facings.items():
        preimage += INVROTMAP[INVSMAP[sticker[1].colour]]

    # convert to Speffz
    for ste, spe in EMAP.items():
        if set(ste) == set(image):
            image = spe
        if set(ste) == set(preimage):
            preimage = spe

    # convert back to standard
    orient_std = ['', '']
    image_std = INVEMAP[image]
    preimage_std = INVEMAP[preimage]
    for sticker in piece.facings.items():
        orient_idx = image_std.index(sticker[0])
        orient_std[orient_idx] = INVROTMAP[INVSMAP[sticker[1].colour]]
    orient_std = ''.join(orient_std)

    # calculate orientation
    orient = 0
    if orient_std == (preimage_std[1] + preimage_std[0]):
        orient = 1
    return (
        ESEQ[0].index(preimage[0]),
        ESEQ[0].index(image[0]),
        orient)


def _corner2state(piece):
    image = piece.location
    preimage = ""
    for sticker in piece.facings.items():
        preimage += INVROTMAP[INVSMAP[sticker[1].colour]]

    # convert to Speffz
    for ste, spe in CMAP.items():
        if set(ste) == set(image):
            image = spe
        if set(ste) == set(preimage):
            preimage = spe

    # convert back to standard
    orient_std = ['', '', '']
    image_std = INVCMAP[image]
    preimage_std = INVCMAP[preimage]
    for sticker in piece.facings.items():
        orient_idx = image_std.index(sticker[0])
        orient_std[orient_idx] = INVROTMAP[INVSMAP[sticker[1].colour]]
    orient_std = ''.join(orient_std)

    # calculate orientation
    orient = 0
    if orient_std == (preimage_std[1:] + preimage_std[0]):
        orient = 1
    if orient_std == (preimage_std[2] + preimage_std[0:2]):
        orient = 2
    return (
        CSEQ[0].index(preimage[0]),
        CSEQ[0].index(image[0]),
        orient)


def decode(cube):
    from pycuber import Cube
    assert isinstance(cube, Cube), type(cube)
    state = Pos(*Pos.SOLVED).copy()
    for piece in cube.children:
        if piece.type == 'centre':
            preimage, image = _center2state(piece)
            state.rp[preimage] = image
        elif piece.type == 'edge':
            preimage, image, orient = _edge2state(piece)
            state.eo[preimage] = orient
            state.ep[preimage] = image
        elif piece.type == 'corner':
            preimage, image, orient = _corner2state(piece)
            state.co[preimage] = orient
            state.cp[preimage] = image
    return state


def _stickers2array(value):
    value = unstickers(value)
    value = value.replace('R', '0')
    value = value.replace('Y', '1')
    value = value.replace('G', '2')
    value = value.replace('W', '3')
    value = value.replace('O', '4')
    value = value.replace('B', '5')
    value = ''.join([
        value[9:12],
        value[21:24],
        value[33:36],
        value[:9],
        value[12:15],
        value[24:27],
        value[36:39],
        value[45:],
        value[15:18],
        value[27:30],
        value[39:42],
        value[18:21],
        value[30:33],
        value[42:45],
    ])
    return value


def encode(pos):
    from .stickers import encode as _encode
    from pycuber.helpers import array_to_cubies
    from pycuber import Cube
    value = _encode(pos)
    value = _stickers2array(value)
    cube = Cube(array_to_cubies(value))
    return cube
