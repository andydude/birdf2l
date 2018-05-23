from birdf2l.models.alg import Alg
from birdf2l.models.pos import Pos
from birdf2l.plugins import speffz


def posid(alg):
    pos = Pos.from_alg(str(Alg(alg).inverse()))
    return speffz.from_id(pos.to_id())
