import sys
import json
from pandas import read_csv, DataFrame
from .annotate import algid, annotate, format_annotation
from argparse import ArgumentParser
from .speed import speed
from .posid import posid
from .generators import generators
from .parallel import metrics
from .annotate import rotate_line
from .models.alg import Alg

def add_arguments(parser):
    return parser
            
def main():
    parser = add_arguments(ArgumentParser())
    options = vars(parser.parse_args(sys.argv[1:]))
    for line in sys.stdin:
        if line.islower():
            continue
        if not line.strip():
            continue
        line = line.strip()
        parts = line.split(',')
        alg = parts[-2]
        alg = str(Alg(alg).mirror_f2l())
        names = parts[-1]
        htm = alg.count(' ') + 1
        id = algid(htm, alg)
        ann = annotate(alg, id, names)
        print(format_annotation(**ann))
        


if __name__ == '__main__':
    main()
