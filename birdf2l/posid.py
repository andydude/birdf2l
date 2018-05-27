from birdf2l.models.alg import Alg
from birdf2l.models.pos import Pos
from birdf2l.plugins import speffz


def posid(alg):
    """
    F2L position identifiers 
    are defined as 
    the Speffz code (short) 
    of the inverse 
    of the given algorithm.
    """
    antialg = str(Alg(alg).inverse())
    pos = Pos.from_alg(antialg)
    return speffz.encode(pos)
