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
| a         | negative one  | -1      |
| b         | negative two  | -2      |
| c         | negative three | -3     |
| d         | negative four | -4      |
| e         | negative five | -5      |
| f         | negative six  | -6      |
| g         | negative seven | -7     |
| h         | negative eight | -8     |
| i         | negative nine | -9      |
| j         | negative ten  | -10     |
| k         | negative eleven | -11   |
| 1Z        | a dozen       | 12      |
| 1A        | a baker's dozen | 13    |
| 1B        | fourteen      | 14      |
| 1C        | fifteen       | 15      |
| 2Z        | twenty-four   | 24      |
| 2A        | twenty-five   | 25      |
| 10Z       | a gross       | 144     |
| 1z        | negative twelve | -12   |
| 1a        | negative thirteen | -13 |

That is, `Z` through `K` are zero through eleven (positive terminal digits),
`a` through `k` are negative one through negative eleven (negative terminal
digits), and `0`-`9`, `X`, `Y` are used for higher-order digits (continuations).

Negative multiples of twelve use `z` as a terminal (e.g. `-12` → `1z`,
`-24` → `2z`); `z` must always follow at least one continuation digit.

This way, you can encode a series of positive and/or negative integers
without need for delimiters. For example, the
[first ten powers of negative two](https://oeis.org/A122803) in base 10:

```
1, -2, 4, -8, 16, -32, 64, -128, 256, -512
```

Dozencoded:

```
AbDh1D2h5DXh19D36h
```

Much better.

## Character Set

| Character(s) | Role | Values |
| ------------ | ---- | ------ |
| `Z`, `A`-`K` | Positive terminal (ones digit) | 0, 1–11 |
| `a`-`k`      | Negative terminal (ones digit) | −1 to −11 |
| `z`          | Negative-zero terminal | −(n×12); must follow a continuation digit |
| `0`-`9`, `X`, `Y` | Continuation (high-order digits) | 0–9, 10, 11 |

## Usage

The reference implementation is Python [dozencode](https://github.com/colinmsaunders/dozencode).
Let us know if you write your own!

```python
from dozencode.dozencode import dozencode, dozdecode
print(dozencode([1, 10, 100, 1000]))    # AJ8D6YD
print(dozdecode("AbDh1D2h5DXh19D36h"))  # [1, -2, 4, -8, 16, -32, 64, -128, 256, -512]
```

## License

Dozencode is released to the public domain on May 23, 2024 by Colin M. Saunders.
