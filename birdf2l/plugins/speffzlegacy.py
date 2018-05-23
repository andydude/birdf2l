from birdf2l.models.pos import Pos

MASK_OE =     "1111                1111                1111            "
MASK_PE =     "     1111                1111                1111       "
MASK_OC =     "          1111                1111                      "
MASK_PC =     "               1111                1111                 "
MASK_PR =     "                                                  111111"
SOLVED_CODE = "0000-ABCD/0000-ABCD/0000-FJNR/0000-UVWX/0000-UVWX/ULFRBD"

ROTSEQ = "ULFRBD"

ESEQ = [
    #123456789ABC
    "ABCDFJNRUVWX",  # 0-orientation
    "QMIELPTHKOSG",  # 1-orientation
]

CSEQ = [
    #12345678
    "ABCDUVWX",  # 0-orientation
    "EQMIGKOS",  # 1-orientation
    "RNJFLPTH",  # 2-orientation
]


def _from_o(ch):
    from binascii import unhexlify
    try:
        if six.PY3:
            return unhexlify('0' + ch)[-1]
        else:
            return ord(unhexlify('0' + ch)[-1])
    except Exception as exc:
        raise

    
def _from_pr(ch):
    try:
        return ROTSEQ.index(ch)
    except Exception as exc:
        raise ValueError("from_pr('{}')".format(ch))

    
def _from_pe(ch):
    return ESEQ[0].index(ch)


def _from_pc(ch):
    return CSEQ[0].index(ch)


def decode(speffz_legacy_id):
    if ' ' in speffz_legacy_id:
        raise NotImplementedError
    try:
        for stop in [19, 39, 49]:
            if len(speffz_legacy) == stop:
                speffz_legacy += SOLVED_CODE[stop:]
        oe, pe, oc, pc, pr = [], [], [], [], []
        for ix, ch in enumerate(list(speffz_legacy)):
            if MASK_OE[ix] == '1':
                oe.append(_from_o(ch))
            if MASK_PE[ix] == '1':
                pe.append(_from_pe(ch))
            if MASK_OC[ix] == '1':
                oc.append(_from_o(ch))
            if MASK_PC[ix] == '1':
                pc.append(_from_pc(ch))
            if MASK_PR[ix] == '1':
                pr.append(_from_pr(ch))
    except Exception as exc:
        return None
    return Pos(oe, pe, oc, pc, pr)


def _to_o(num):
    from binascii import hexlify
    try:
        ch = hexlify(chr(num).encode('latin1')).decode('latin1')[-1].upper()
    except Exception as exc:
        raise
    return ord(ch)


def _to_pr(num):
    try:
        return ROTSEQ[num]
    except Exception as exc:
        raise ValueError("to_pr({})".format(num))

    
def _to_pe(num):
    return ESEQ[0][num]


def _to_pc(num):
    return CSEQ[0][num]


def encode(pos):
    if not isinstance(pos, Pos):
        raise TypeError("input must be a Pos object")
    try:
        speffz_legacy = bytearray(SOLVED_CODE.encode('latin1'))
        oe = list(reversed(pos.eo))
        pe = list(reversed(pos.ep))
        oc = list(reversed(pos.co))
        pc = list(reversed(pos.cp))
        pr = list(reversed(pos.rp))
        for ix, ch in enumerate(list(speffz_legacy)):
            if MASK_OE[ix] == '1':
                speffz_legacy[ix] = _to_o(oe.pop())
            if MASK_PE[ix] == '1':
                speffz_legacy[ix] = ord(_to_pe(pe.pop()))
            if MASK_OC[ix] == '1':
                speffz_legacy[ix] = _to_o(oc.pop())
            if MASK_PC[ix] == '1':
                speffz_legacy[ix] = ord(_to_pc(pc.pop()))
            if MASK_PR[ix] == '1':
                speffz_legacy[ix] = ord(_to_pr(pr.pop()))
        speffz_legacy = speffz_legacy.decode('latin1')
        for stop in [19, 39, 49]:
            if speffz_legacy.endswith(SOLVED_CODE[stop:]):
                speffz_legacy = speffz_legacy[:-len(SOLVED_CODE[stop:])]
    except Exception as exc:
        raise
        #print(repr(exc))
        #return None
    return speffz_legacy
