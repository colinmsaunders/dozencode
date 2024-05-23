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
| K         | eleven        | 11      |
| Az        | a dozen       | 12      |
| Aa        | a baker's dozen | 13    |
| Azz       | a gross       | 144     |
| Y         | negative one  | -1      |
| X         | negative two  | -2      |
| Xz        | negative twelve | -12   |

That is, `Z` is zero, `A` through `K` are one through eleven, `Y` through
`O` is negative one through negative 11, `z` and `a` through `k` are used
for digits beyond the ones.

This way, you can encode a series of positive and/or negative integers
without need for delimters. For example, the
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

```python
from dozencode.dozencode import dozencode, dozdecode
print(dozencode([1, 10, 100, 1000]))    # AJHdFkd 
print(dozdecode("AXDRAdXhEdPhAid"))     # [1, -2, 4, -8, 16, -32, 64, -128, 256]
```