C_MAP = {
    ('0', 'A'): 'A',
    ('1', 'A'): 'R',
    ('2', 'A'): 'E',
    ('0', 'B'): 'B',
    ('1', 'B'): 'N',
    ('2', 'B'): 'Q',
    ('0', 'C'): 'C',
    ('1', 'C'): 'J',
    ('2', 'C'): 'M',
    ('0', 'D'): 'D',
    ('1', 'D'): 'F',
    ('2', 'D'): 'I',
    ('0', 'U'): 'U',
    ('1', 'U'): 'L',
    ('2', 'U'): 'G',
    ('0', 'V'): 'V',
    ('1', 'V'): 'P',
    ('2', 'V'): 'K',
    ('0', 'W'): 'W',
    ('1', 'W'): 'T',
    ('2', 'W'): 'O',
    ('0', 'X'): 'X',
    ('1', 'X'): 'H',
    ('2', 'X'): 'S',
    ('.', '.'): '_',
}


E_MAP = {
    ('0', 'A'): 'a',
    ('1', 'A'): 'q',
    ('0', 'B'): 'b',
    ('1', 'B'): 'm',
    ('0', 'C'): 'c',
    ('1', 'C'): 'i',
    ('0', 'D'): 'd',
    ('1', 'D'): 'e',
    ('0', 'F'): 'f',
    ('1', 'F'): 'l',
    ('0', 'J'): 'j',
    ('1', 'J'): 'p',
    ('0', 'N'): 'n',
    ('1', 'N'): 't',
    ('0', 'R'): 'r',
    ('1', 'R'): 'h',
    ('0', 'U'): 'u',
    ('1', 'U'): 'k',
    ('0', 'V'): 'v',
    ('1', 'V'): 'o',
    ('0', 'W'): 'w',
    ('1', 'W'): 's',
    ('0', 'X'): 'x',
    ('1', 'X'): 'g',
    ('.', '.'): '_',
}

def is_f2l(jop, kop):
    if jop[0] == 'f' and \
       jop[2:] == 'nr' and \
       kop[0] == 'U' and \
       kop[2:] == 'WX' and \
       (jop[1] != 'j' or \
        kop[1] != 'V'):
        return True
    return False

def from_e1(o, p):
    return E_MAP[(o, p)]
def from_c1(o, p):
    return C_MAP[(o, p)]
def from_q4(s, f):
    r = ''
    if len(s) == 9:
        parts = s.split('-')
        for o, p in zip(parts[0], parts[1]):
            r += f(o, p)
    else:
        raise ValueError
    return r

def from_legacy(speffz_legacy_id):
    parts = speffz_legacy_id.split('/')
    if len(parts) == 2:
        eop = parts[0]
        cop = parts[1]
        eop = from_q4(eop, from_e1)
        cop = from_q4(cop, from_c1)
        speffz_id = ''.join([
            cop[0], eop[0],
            cop[1], eop[1],
            cop[2], eop[2],
            cop[3], eop[3],
        ])
    elif len(parts) == 4:
        eop = parts[0]
        cop = parts[1]
        jop = parts[2]
        kop = parts[3]
        assert len(jop) == len(kop)
        eop = from_q4(eop, from_e1)
        cop = from_q4(cop, from_c1)
        jop = from_q4(jop, from_e1)
        kop = from_q4(kop, from_c1)
        ceop = ''.join([
            cop[0], eop[0],
            cop[1], eop[1],
            cop[2], eop[2],
            cop[3], eop[3],
        ])
        if is_f2l(jop, kop):
            speffz_id = '/'.join([ceop, kop[1] + jop[1]])
        else:
            jkop = ''.join([
                kop[0], jop[0],
                kop[1], jop[1],
                kop[2], jop[2],
                kop[3], jop[3],
            ])
            speffz_id = '/'.join([ceop, jkop])

    else:
        raise ValueError
    return speffz_id


def to_legacy(spefz_id):
    (co, cp, eo, ep) = list(spefz_id)
    co = [key for key, value in CO_MAP.items() if value == co][0]
    eo = [key for key, value in EO_MAP.items() if value == eo][0]
    cp = [key for key, value in CP_MAP.items() if value == cp][0]
    ep = [key for key, value in EP_MAP.items() if value == ep][0]
    speffz_legacy_id = '{}-{}/{}-{}'.format(eo, ep, co, cp)
    return speffz_legacy_id


def decode(speffz_id):
    from .speffzlegacy import decode as _decode
    speffz_legacy_id = to_legacy(speffz_id)
    #print(speffz_legacy_id)
    pos = _decode(speffz_legacy_id)
    return pos


def encode(pos):
    from .speffzlegacy import encode as _encode
    speffz_legacy_id = _encode(pos)
    #print(speffz_legacy_id)
    speffz_id = from_legacy(speffz_legacy_id)
    return speffz_id
