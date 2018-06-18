import csv

UNPACK_MAP = {
    'r': "R2", 'P': "R'", 'R': "R",
    'l': "L2", '1': "L'", 'L': "L",
    'u': "U2", 'n': "U'", 'U': "U",
    'd': "D2", 'p': "D'", 'D': "D",
    'f': "F2", 'E': "F'", 'F': "F",
    'b': "B2", 'q': "B'", 'B': "B",
}

def unpackify(c):
    if c in UNPACK_MAP:
        c = UNPACK_MAP[c]
    return c

with open("/home/ajr/cubecode/fixtures/alg_raw.txt", "w") as writer:
    with open("/home/ajr/Birdflu/seed_data/raw_alg_bulk.csv") as reader:
        rows = csv.reader(reader)
        for row in rows:
            encoded_alg = row[6]
            alg = ' '.join(map(unpackify, list(encoded_alg)))
            writer.write(alg + '\n')                       
