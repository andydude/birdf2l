'''

Definition of Unhanding (Hand-2-Face):

1. Group Expansion
   - Replace `(R U)3` with `R U R U R U`. Getting rid
     of groups allows us to assume they don't exist.
2. Notation Substitution
   - Replace `Rw` with `r` and so on. There are many
     common notation systems with identical symantics.     
3. Notation Expansion
   - Replace `r` with `x' L'`, `M` with `x' L' R", and so on.
     This makes the unhanding step easier.
4. Rotation Deletion (Unhanding)
   - To get rid of rotations, we need substitution tables
     for all possible rotations. This is easily created
     by the position class (Pos) using get_rotation().

Definition of Canonicalization (requires Unhanding):

5. Parallel Compression
   - It is common while mining to encounter sequences
     of steps like `L R L R L R` which is equivalent to
     `L' R'`, but require advanced recognition.
6. Parallel Collation
   - It is common to see parallel moves written either
     `L R` or `R L`, and in this step we enforce that they
     are written in alphabetical order, which implies
     that both are written `L R`. The other sides are
     ordered `B F` not `F B`, and `D U` not `U D`.
7. Optimization
   - It is common while mining to encounter sequences
     of steps like `L2 R2 B2 F2 L2 R2 B2 F2` which are
     no-ops but can appear to be doing something.

Definition of Adjusted-Canonicalization:

8a. Adjust Upper Face for First Two Layers (AUF-F2L)
    - Generally done with `U` moves before the algorithm.
8b. Adjust Upper Face to Orient Last Layer Adjust Upper Face (AUF-OLL)
    - Generally done with `y` moves before the algorithm.
    - Must be one of the 8 Birdflu orientations.
8c. Adjust Upper Face to Permute Last Layer Adjust Upper Face (AUF-PLL)
    - Generally done with `y` moves before the algorithm.
    - Diagonal corner swaps must be between B and D.
    - Adjacent corner swaps must be between C and D.
9. Return the algorithm if found in the database.
'''
import re
from pandas import read_csv

from birdf2l.models.alg import Alg
from birdf2l.models.pos import Pos
from birdf2l.parallel import is_alt, is_opp

FACES = "ULFRBD"
FACES2 = "ULFDRB"
ROTATIONS = ['x', 'y', 'z']
TRANSLATIONS = {}

NOTATIONS = read_csv('fixtures/subs_notation.csv')
UNHANDINGS = read_csv('fixtures/subs_unhand.csv')
COLLATIONS = read_csv('fixtures/subs_collate.csv')
OPTIMIZATIONS = read_csv('fixtures/subs_optimize.csv')


_repetition_re = re.compile(
    r"\((?P<alg>[\w\s\']+)\)(?P<num>\d)")
_non_group_re = re.compile(
    r"[^\w\s\']")
def _expand_repetition(alg_code):
    while True:
        match = _repetition_re.search(alg_code)
        if not match:
            break
        repnum = match.group('num')
        repnum = int(repnum)
        subalg = match.group('alg')
        subalg += " "
        alg_code = alg_code.replace(match.group(0), subalg*repnum)
    alg_code = _non_group_re.sub('', alg_code)
    alg_code = alg_code.strip()
    return alg_code


def _expand_notations(alg):
    for _, d in NOTATIONS.transpose().to_dict().items():
        alg = alg.replace(d['pattern'] + ' ', d['replace'] + ' ')
    return alg


def _expand_unhanding(alg):    
    for _, d in UNHANDINGS.transpose().to_dict().items():
        alg = alg.replace(d['pattern'] + ' ', d['replace'] + ' ')
    return alg


def expand(alg, unhanding=False):
    alg += ' '
    alg = _expand_groups(alg)
    alg = _expand_notations(alg)
    if unhanding:
        alg = _expand_unhanding(alg)
    return alg[:-1]


class Unhander(object):
    
    def __init__(self):
        self.rot = ''
        self.alg = ''
        self.pos = Pos(*Pos.SOLVED)

    def unhand_step(self, step):
        return FACES[self.pos.rp[FACES.index(step[0])]]
    
    def step_rot(self, step):
        self.rot += ' ' + step
        self.rot = optimize(self.rot)
        self.rot = self.rot.strip()

    def step_alg(self, step):
        step = self.unhand_step(step)
        self.alg += ' ' + step
        self.alg = self.alg.strip()
    
    def step(self, step):
        if not len(step):
            return
        if step[0] in ROTATIONS:
            self.step_rot(step)
        else:
            self.step_alg(step)
        self.pos = self.pos.from_step(step)

            
def unhand(alg):
    """
    """
    alg = expand(alg)
    unhander = Unhander()
    for step in alg.split(' '):
        for substep in step.split(' '):
            unhander.step(substep)
    return unhander.alg.strip()


def _parallel_compress(alg):
    return alg

def _parallel_collate(alg):
    for _, d in COLLATIONS.transpose().to_dict().items():
        alg = alg.replace(d['pattern'] + ' ', d['replace'] + ' ')
    return alg

def _parallel_optimize(alg):
    for _, d in OPTIMIZATIONS.transpose().to_dict().items():
        alg = alg.replace(d['pattern'] + ' ', d['replace'] + ' ')
    return alg

def optimize(alg):
    """
    """
    alg += ' '
    alg = _parallel_compress(alg)
    alg = _parallel_collate(alg)
    alg = _parallel_optimize(alg)
    return alg


def canonicalize(alg):
    """
    """
    return optimize(unhand(alg))


def auf_f2l(alg):
    pass


def auf_oll(alg):
    pass


def auf_pll(alg):
    pass
