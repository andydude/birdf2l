import sys
import json
from pandas import read_csv, DataFrame
from .annotate import annotate, format_annotation
from argparse import ArgumentParser
from .speed import speed
from .posid import posid
from .generators import generators
from .parallel import metrics
from .annotate import rotate_line

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
        rotate_line(line)


if __name__ == '__main__':
    main()
