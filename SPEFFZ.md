In Speffz, every sticker has a name:

```
         A  a  B
         d  U  b
         D  c  C
E  e  F  I  i  J  M  m  N  Q  q  R
h  L  f  l  F  j  p  R  n  t  B  r
H  g  G  L  k  K  P  o  O  T  s  S
         U  u  V
         x  D  v
         X  w  W
```

Last Layer (LL) algorithms can be described by IDs of the form

```
{A}{a}{B}{b}{C}{c}{D}{d}
```

First Two Layer (F2L) algorithms can be described by Anti-IDs of the form

```
{A}{a}{B}{b}{C}{c}{D}{d}/{V}{j}
```

Some cube systems use sticker rotation, some use
matrix rotation, and some use a pair of IDs:

- Piece ID (PID) to refer to a given set of sticker colors,
- Orientation ID (OID) to refer to where each sticker is pointing.

Since Speffz uniquely names each sticker, we can compress these
two pieces of information into a single letter. For corners:

```
| OID | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | - | - | - | - | - | - | - | - |
|  0  | A | B | C | D | U | V | W | X |
|  1  | R | N | J | F | L | P | T | H |
|  2  | E | Q | M | I | G | K | O | S |
```

And for edges:

```
| OID | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
| --- | - | - | - | - | - | - | - | - | - | - | - | - |
|  0  | a | b | c | d | f | j | n | r | u | v | w | x |
|  1  | q | m | i | e | l | p | t | h | k | o | s | g |
```

Some pieces of code refer to `SpeffzLegacy`, which is based on this, but is broken into two parts, `"2220-ABCD"` would be the `SpeffzLegacy` which corresponds to `"EQMD"` in `Speffz`.

