import sys
import json
from pandas import read_csv, DataFrame
from .annotate import annotate, format_annotation
from argparse import ArgumentParser
from .speed import speed
from .posid import posid
from .generators import generators
from .parallel import metrics


ALG = read_csv("fixtures/alg.csv", dtype=str, keep_default_na=False)
PAT = read_csv("fixtures/pat.csv", dtype=str, keep_default_na=False)


def algid(nmoves):    
    ALPHA = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return 'V-{}{}'.format(
        ALPHA[nmoves], '?')


def add_arguments(parser):
    return parser


def main():
    pats = list(PAT.transpose().to_dict().values())
    patids = [pat['patid'] for pat in pats]
    parser = add_arguments(ArgumentParser())
    options = vars(parser.parse_args(sys.argv[1:]))
    lines = sys.stdin.read()
    for line in lines.split('\n'):
        if line.islower():
            continue
        if not line.strip():
            continue
        parts = line.split(',')
        try:
            if len(parts) == 0:
                raise ValueError
            elif len(parts) == 1:

                # 1 column means: alg
                alg = parts[0]
                names = ''
            else:
                
                # 2+ columns mean: alg, names
                alg = parts[-2]
                names = parts[-1]

            alg0 = alg
            if alg0.startswith("U"):
                alg0 = alg0[alg0.index(" ") + 1:]
            for us in ['', "U ", "U2 ", "U' "]:
                alg = us + alg0
                htm = alg.count(' ') + 1
                ann = annotate(alg, algid(htm), names)
                if ann['patid'] in patids:
                    print(format_annotation(**ann))
                    break
                else:
                    alg = 'U ' + alg
            else:
                print("# could not find F2L pattern match for alg " + alg)
        except Exception as exc:
            print("# " + repr(exc))
            raise
            print(line)


if __name__ == '__main__':
    main()
