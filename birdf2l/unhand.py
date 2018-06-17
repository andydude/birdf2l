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
''' 

from birdf2l.models.alg import Alg
from birdf2l.models.parallel import is_alt, is_opp
from birdf2l.models.pos import Pos

ROTATIONS = ['x', 'y', 'z']
TRANSLATIONS = {}
OPTIMIZATIONS = read_csv('fixtures/subs_optim.csv')
UNHANDINGS = read_csv('fixtures/subs_unhand.csv')


class Unhander(object):
    
    def __init__(self):
        self.rot = ''
        self.alg = ''

    def unhand1(self, step):
        step = TRANSLATIONS[self.rot][step[0]] + step[1:]
        return step
    
    def step_rot(self, step):
        self.rot += ' ' + step
        self.rot = optimize(self.rot)
        self.rot = self.rot.strip()
    
    def step_alg(self, step):
        step = self.unhand1(step)
        self.alg += ' ' + step
        self.alg = self.alg.strip()
    
    def step(self, step):
        if not len(step):
            return
        if step[0] in ROTATIONS:
            self.step_rot(step)
        else:
            self.step_alg(step)

            
def unhand(alg):
    helper = Unhander()
    for step in alg.split(' '):
        if step in CANON.keys():
            step = CANON[step]
        for substep in step.split(' '):
            helper.step(substep)
    return helper.alg.strip()


def optimize(alg):
    alg += ' '
    return alg


def canonicalize(alg):
    alg = unhand(alg)
    alg = alg
    return alg
