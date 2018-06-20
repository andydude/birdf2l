from collections import namedtuple


class AlgIter(object):
    """
    Helper for iterating over algorithms.
    """

    def __init__(self, alg):
        self.alg = alg
        self.i = -1

    def __next__(self):
        self.i += 1
        return self.alg.moves[self.i]

    next = __next__


class AlgStep(namedtuple('AlgStep', 'name')):
    """
    Helper for inverting algorithms.
    Pycuber calls this class `Step`.
    """

    @property
    def face(self):
        return self.name[0]

    @property
    def is_cw(self):
        return self.name[1:] == ""

    @property
    def is_ccw(self):
        return self.name[-1] == "'"

    @property
    def is_180(self):
        return self.name[1:] == "2"

    def angle(self):
        if self.is_cw:
            return 1
        elif self.is_ccw:
            return -1
        elif self.is_180:
            return 2
        elif self.name.endswith("'2"):
            return 2
        else:
            raise ValueError

    def inverse(self):
        if self.is_cw:
            return self.face + "'"
        elif self.is_180:
            return self.name
        elif self.is_ccw:
            return self.face
        else:
            raise ValueError(self.name)



class Alg(object):

    def __init__(self, moves):
        if isinstance(moves, str):
            moves = moves.split()
        if not isinstance(moves, list):
            raise ValueError
        self.moves = moves

    def __iter__(self):
        return AlgIter(self)

    def __str__(self):
        return ' '.join(self.moves)

    @classmethod
    def from_code(cls, code):
        """
        Pycuber calls this ``.
        Roofpig calls this `_make_move`.
        """
        pass

    def __reversed__(self):
        return Alg(reversed(self.moves))

    def inverse(self):
        """
        Backwards and negative.
        Pycuber calls this `reverse`.
        """
        return Alg([
            AlgStep(move).inverse()
            for move in reversed(self.moves)])

    def mirror_ext(self, swap, same):
        mirmoves = []
        half = len(swap)/2
        for move in self.moves:
            step = AlgStep(move).inverse()
            if step[0] in swap:
                step = swap[(swap.index(step[0]) + half) % len(swap)] + step[1:]
            mirmoves.append(step)
        return Alg(mirmoves)
            
    def mirror_x(self):
        """
        Converts R to L'.
        """
        return self.mirror_ext("RL", "UFDB")

    def mirror_y(self):
        """
        Converts U to D'.
        """
        return self.mirror_ext("UD", "LFRB")

    def mirror_z(self):
        """
        Converts F to B'.
        """
        return self.mirror_ext("FB", "ULDR")

    def mirror_f2l(self):
        """
        Converts R to F' and L to B'
        """
        return self.mirror_ext("RLFB", "UD")

    @classmethod
    def random(cls):
        pass
