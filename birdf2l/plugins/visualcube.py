import os
import requests


def visualcube_download(alg, patid):
    import requests
    response = requests.get(
        url="https://www.speedsolving.com/wiki/extensions/algdb/vcube/visualcube.php",
        params={
            'fmt': 'png',
            'bg': 'w',
            'size': '128',
            'sch': 'ygrwbo',
            'stage': 'f2l',
            'view': '3d',
            'case': alg})
    filename = "/home/ajr/birdf2l/img/{}.png".format(patid)
    if os.path.exists(filename):
        return
    with open(filename, "w") as writer:
        writer.write(response.content)


COL_PAT = 1
COL_ALG = 13

def main():
    with open("/home/ajr/birdf2l/fixtures/pat.csv") as reader:
        for line in reader:
            line = line.split()
            row = line.split(',')
            if len(row) < 10:
                continue
            if ' ' not in row[COL_ALG]:
                continue
            print("pat = ", row[COL_PAT], "alg = ", row[COL_ALG])
            visualcube_download(row[COL_ALG], row[COL_PAT])


if __name__ == '__main__':
    main()
