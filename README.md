# birdf2l
Speedcubing database

## Algorithm Annotation

The `annotate` command takes a hand algorithm as input, and outputs an F2L
if it is F2L, and outputs other interesting facts, like Speffz ID and number of moves.

```
$ echo "U R U' R'" | python -m birdf2l.annotate --json
{
    "alg": "U R U' R'",
    "algid": "V-D3",
    "cat": "f2l",
    "cllnames": [],
    "cllnum": null,
    "ellnames": [],
    "ellnum": null,
    "f2lcubefreak": "I2",
    "f2lnum": 1,
    "f2lspeedsolving": 1,
    "f2lpatid": "Jb",
    "gen": 2,
    "gens": "RU",
    "handalgs": [],
    "invalg": "R U R' U'",
    "invposid": "abdp/IBKA/Mi",
    "miralg": "U' F' U F",
    "mirpatid": "Mi",
    "mirposid": "abdp/IBKA/Mi",
    "notes": ["Anti-Sexy"]
    "metrics": {
        "htm": 4,
        "qtm": 4,
        "stm": 4
    },
    "ollnames": [],
    "ollnum": null,
    "pllnames": [],
    "pllnum": null,
    "posid": "jacd/NAPD/Jb",
    "speed": 2.88
}
```
