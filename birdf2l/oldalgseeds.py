from argparse import ArgumentParser
import sys

DEFAULT_INDEX = 'fixtures/algseeds/all.csv'

def add_arguments(parser):
    parser.add_argument('--indexfile', default=DEFAULT_INDEX)
    parser.add_argument('--csv', action='store_true')
    parser.add_argument('--json', action='store_true')
    return parser


def main():
    parser = add_arguments(ArgumentParser())
    options = vars(parser.parse_args(sys.argv[1:]))
    with open(options.get('indexfile', DEFAULT_INDEX)) as reader:
        filenames = reader.read().split('\n')
    if options.get('csv', False):
        print("htm,alg,notes")
    for filename in filenames:
        if not filename:
            continue
        with open("fixtures/algseeds/" + filename) as reader:
            lines = reader.read()
            for line in lines.split('\n'):
                if line.startswith('alg'):
                    continue
                if not line.strip():
                    continue
                parts = line.split(',')
                try:
                    assert len(parts) == 2, parts
                    # 2+ columns mean: alg, names
                    alg = parts[-2]
                    names = parts[-1]
                        
                    htm = alg.count(' ') + 1
                    if options.get('csv', False):
                        print(','.join([
                            str(htm), alg, names]))
                except Exception as exc:
                    print("# " + repr(exc))
                    raise
                    print(line)

if __name__ == '__main__':
    main()
