import six
from collections import namedtuple
from logging import getLogger

LOG = getLogger()

PosBase = namedtuple('Pos', 'co cp eo ep rp')


class Pos(PosBase):
    """
    Represents cube state.
    """

    SOLVED = PosBase(
        co=(0, 0, 0, 0, 0, 0, 0, 0),
        cp=(0, 1, 2, 3, 4, 5, 6, 7),
        eo=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ep=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
        rp=(0, 1, 2, 3, 4, 5))

    U = PosBase(
        co=(0, 0, 0, 0, 0, 0, 0, 0),
        cp=(1, 2, 3, 0, 4, 5, 6, 7),
        eo=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ep=(1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11),
        rp=(0, 1, 2, 3, 4, 5))

    R = PosBase(
        co=(0, 1, 2, 0, 0, 1, 2, 0),
        cp=(0, 6, 1, 3, 4, 2, 5, 7),
        eo=(0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
        ep=(0, 6, 2, 3, 4, 1, 9, 7, 8, 5, 10, 11),
        rp=(0, 1, 2, 3, 4, 5))

    F = PosBase(
        co=(0, 0, 1, 2, 1, 2, 0, 0),
        cp=(0, 1, 5, 2, 3, 4, 6, 7),
        eo=(0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0),
        ep=(0, 1, 5, 3, 2, 8, 6, 7, 4, 9, 10, 11),
        rp=(0, 1, 2, 3, 4, 5))

    L = PosBase(
        co=(2, 0, 0, 1, 2, 0, 0, 1),
        cp=(3, 1, 2, 4, 7, 5, 6, 0),
        eo=(0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0),
        ep=(0, 1, 2, 4, 11, 5, 6, 3, 8, 9, 10, 7),
        rp=(0, 1, 2, 3, 4, 5))

    B = PosBase(
        co=(1, 2, 0, 0, 0, 0, 1, 2),
        cp=(7, 0, 2, 3, 4, 5, 1, 6),
        eo=(1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
        ep=(7, 1, 2, 3, 4, 5, 0, 10, 8, 9, 6, 11),
        rp=(0, 1, 2, 3, 4, 5))

    D = PosBase(
        co=(0, 0, 0, 0, 0, 0, 0, 0),
        cp=(0, 1, 2, 3, 5, 6, 7, 4),
        eo=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ep=(0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8),
        rp=(0, 1, 2, 3, 4, 5))

    x = PosBase(
        co=(2, 1, 2, 1, 2, 1, 2, 1),
        cp=(7, 6, 1, 0, 3, 2, 5, 4),
        eo=(1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1),
        ep=(10, 6, 0, 7, 3, 1, 9, 11, 2, 5, 8, 4),
        rp=(5, 4, 2, 3, 0, 1))

    y = PosBase(
        co=(0, 0, 0, 0, 0, 0, 0, 0),
        cp=(1, 2, 3, 0, 7, 4, 5, 6),
        eo=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ep=(1, 2, 3, 0, 7, 4, 5, 6, 11, 8, 9, 10),
        rp=(0, 1, 4, 5, 3, 2))

    z = PosBase(
        co=(1, 2, 1, 2, 1, 2, 1, 2),
        cp=(1, 6, 5, 2, 3, 4, 7, 0),
        eo=(0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1),
        ep=(6, 9, 5, 1, 2, 8, 10, 0, 4, 11, 7, 3),
        rp=(2, 3, 1, 0, 4, 5))

    def __call__(self, action):
        assert isinstance(action, PosBase)
        return type(self)(
            ep=tuple(action.ep[self.ep[ix]]
                     for ix in range(12)),
            cp=tuple(action.cp[self.cp[ix]]
                     for ix in range(8)),
            eo=tuple((action.eo[self.ep[ix]] + self.eo[ix]) % 2
                     for ix in range(12)),
            co=tuple((action.co[self.cp[ix]] + self.co[ix]) % 3
                     for ix in range(8)),
            rp=tuple(action.rp[self.rp[ix]]
                     for ix in range(6)))
    
    @classmethod
    def from_alg(cls, steps):
        assert isinstance(steps, six.string_types)
        self = cls(*cls.SOLVED)
        for step in steps.split(' '):
            try:
                self = self.from_step(step)
            except Exception as exc:
                LOG.exception(exc)
                raise
        return self

    def from_step(self, step):
        return self(getattr(type(self), step))

    def copy(self):
        return type(self)(
            co=list(self.co),
            cp=list(self.cp),
            eo=list(self.eo),
            ep=list(self.ep),
            rp=list(self.rp))

    def is_solved(self):
        return tuple(self) == tuple(type(self).SOLVED)

    @classmethod
    def init_alg(cls, definiendum, definiens):
        setattr(cls, definiendum, cls.from_alg(definiens))

    @classmethod
    def init(cls):
        setattr(cls, "", cls.SOLVED)
        for move in ["U", "R", "F", "D", "L", "B", "x", "y", "z"]:
            cls.init_alg(move + "2", "{} {}".format(move, move))
            cls.init_alg(move + "'", "{} {} {}".format(move, move, move))

    # END CORE CLASS

    def is_f2l(self):
        try:
            # cross
            assert self.eo[8] == 0
            assert self.eo[9] == 0
            assert self.eo[10] == 0
            assert self.eo[11] == 0
            assert self.ep[8] == 8
            assert self.ep[9] == 9
            assert self.ep[10] == 10
            assert self.ep[11] == 11

            # U slot
            assert self.eo[4] == 0
            assert self.ep[4] == 4
            assert self.co[4] == 0
            assert self.cp[4] == 4
            
            # W slot
            assert self.eo[6] == 0
            assert self.ep[6] == 6
            assert self.co[6] == 0
            assert self.cp[6] == 6
            
            # X slot
            assert self.eo[7] == 0
            assert self.ep[7] == 7
            assert self.co[7] == 0
            assert self.cp[7] == 7
            
            return True
        except:
            return False

    def is_f2l_u(self):
        try:
            # cross
            assert self.eo[8] == 0
            assert self.eo[9] == 0
            assert self.eo[10] == 0
            assert self.eo[11] == 0
            assert self.ep[8] == 8
            assert self.ep[9] == 9
            assert self.ep[10] == 10
            assert self.ep[11] == 11

            # V slot
            assert self.eo[5] == 0
            assert self.ep[5] == 5
            assert self.co[5] == 0
            assert self.cp[5] == 5
            
            # W slot
            assert self.eo[6] == 0
            assert self.ep[6] == 6
            assert self.co[6] == 0
            assert self.cp[6] == 6
            
            # X slot
            assert self.eo[7] == 0
            assert self.ep[7] == 7
            assert self.co[7] == 0
            assert self.cp[7] == 7
            
            return True
        except:
            return False

    def is_f2l_w(self):
        try:
            assert self.eo[4] == 0
            assert self.eo[5] == 0
            assert self.eo[7] == 0
            assert self.eo[8] == 0
            assert self.eo[9] == 0
            assert self.eo[10] == 0
            assert self.eo[11] == 0
            assert self.ep[4] == 4
            assert self.ep[5] == 5
            assert self.ep[7] == 7
            assert self.ep[8] == 8
            assert self.ep[9] == 9
            assert self.ep[10] == 10
            assert self.ep[11] == 11
            assert self.co[4] == 0
            assert self.co[5] == 0
            assert self.co[7] == 0
            assert self.cp[4] == 4
            assert self.cp[5] == 5
            assert self.cp[7] == 7
            return True
        except:
            return False

    def is_f2l_x(self):
        try:
            assert self.eo[4] == 0
            assert self.eo[5] == 0
            assert self.eo[6] == 0
            assert self.eo[8] == 0
            assert self.eo[9] == 0
            assert self.eo[10] == 0
            assert self.eo[11] == 0
            assert self.ep[4] == 4
            assert self.ep[5] == 5
            assert self.ep[6] == 6
            assert self.ep[8] == 8
            assert self.ep[9] == 9
            assert self.ep[10] == 10
            assert self.ep[11] == 11
            assert self.co[4] == 0
            assert self.co[5] == 0
            assert self.co[6] == 0
            assert self.cp[4] == 4
            assert self.cp[5] == 5
            assert self.cp[6] == 6
            return True
        except:
            return False

    def is_f2l_uv(self):
        try:
            # cross
            assert self.eo[8] == 0
            assert self.eo[9] == 0
            assert self.eo[10] == 0
            assert self.eo[11] == 0
            assert self.ep[8] == 8
            assert self.ep[9] == 9
            assert self.ep[10] == 10
            assert self.ep[11] == 11

            assert self.eo[6] == 0
            assert self.ep[6] == 6
            assert self.co[6] == 0
            assert self.cp[6] == 6
            
            assert self.eo[7] == 0
            assert self.ep[7] == 7
            assert self.co[7] == 0
            assert self.cp[7] == 7
            return True
        except:
            return False

    def is_f2l_vw(self):
        try:
            # cross
            assert self.eo[8] == 0
            assert self.eo[9] == 0
            assert self.eo[10] == 0
            assert self.eo[11] == 0
            assert self.ep[8] == 8
            assert self.ep[9] == 9
            assert self.ep[10] == 10
            assert self.ep[11] == 11

            assert self.eo[4] == 0
            assert self.eo[6] == 0
            assert self.ep[4] == 4
            assert self.ep[6] == 6
            assert self.co[4] == 0
            assert self.co[6] == 0
            assert self.cp[4] == 4
            assert self.cp[6] == 6
            return True
        except:
            return False

    def is_f2l_vx(self):
        try:
            assert self.eo[4] == 0
            assert self.eo[7] == 0
            assert self.eo[8] == 0
            assert self.eo[9] == 0
            assert self.eo[10] == 0
            assert self.eo[11] == 0
            assert self.ep[4] == 4
            assert self.ep[7] == 7
            assert self.ep[8] == 8
            assert self.ep[9] == 9
            assert self.ep[10] == 10
            assert self.ep[11] == 11
            assert self.co[4] == 0
            assert self.co[7] == 0
            assert self.cp[4] == 4
            assert self.cp[7] == 7
            return True
        except:
            return False
        
    def is_f2l_xu(self):
        return False
    
    def is_f2l_wx(self):
        return False
    
    def is_f2l_uw(self):
        return False


Pos.init()
