# Dozencode

## Introducing Dozencode

Dozencode (pronounced DUZ-encode) is a duodecimal number system, with
a couple of nifty features that make it nice for transmitting encoded
integers. 

By way of example:

| Dozencode | Pronunciation | Base 10 |
| --------- | ------------- | ------- |
| Z         | zero          | 0       |

| A         | one           | 1       |
| B         | two           | 2       |
| C         | three         | 3       |
| D         | four          | 4       |
| E         | five          | 5       |
| F         | six           | 6       |
| G         | seven         | 7       |
| H         | eight         | 8       |
| I         | nine          | 9       |
| J         | ten           | 10      |
| K         | eleven        | 11      |

| Y         | negative one  | -1      |
| X         | negative two  | -2      |
| W         | negative three | -3      |
| V         | negative four | -4     |
| U         | negative five | -5      |
| T         | negative six  | -6      |
| S         | negative seven | -7      |
| R         | negative eight | -8      |
| Q         | negative nine | -9      |
| P         | negative ten  | -10     |
| O         | negative eleven  | -11    |

| Az        | a dozen       | 12      |
| Aa        | a baker's dozen | 13    |
| Ab        | fourteen      | 14      |
| Ac        | fifteen      | 14      |
| Bz        | twenty-four   | 24      |
| Ba        | twenty-five   | 25      |
| Azz       | a gross       | 144     |

| Yz        | negative twelve | -12   |
| Ya        | negative thirteen | -13   | 

That is, `Z` is zero, `A` through `K` are one through eleven, `Y` through
`O` is negative one through negative 11, `z` and `a` through `k` are used
for digits beyond the ones.

This way, you can encode a series of positive and/or negative integers
without need for delimiters. For example, the
[first nine powers of negative two](https://oeis.org/A122803) in base 10:

```
1, -2, 4, -8, 16, -32, 64, -128, 256
```

Dozencoded:

```
AXDRAdXhEdPhAid
```

Much better.

## Usage

The reference implementation is Python [dozencode](https://github.com/colinmsaunders/dozencode).
Let us know if you write your own!

```python
from dozencode.dozencode import dozencode, dozdecode
print(dozencode([1, 10, 100, 1000]))    # AJHdFkd 
print(dozdecode("AXDRAdXhEdPhAid"))     # [1, -2, 4, -8, 16, -32, 64, -128, 256]
```

## License

Dozencode is released to the public domain on May 23, 2024 by Colin M. Saunders.
