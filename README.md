# Dozencode

## Introducing Dozencode

Dozencode (pronounced DUZ-encode) is a duodecimal number system, with
a couple of nifty features that make it nice for transmitting encoded
integers.

`Z` through `K` are zero through eleven (positive terminal digits),
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

### Python

The reference implementation is Python [dozencode](https://github.com/colinmsaunders/dozencode).

```python
from dozencode.dozencode import dozencode, dozdecode
print(dozencode([1, 10, 100, 1000]))    # AJ8D6YD
print(dozdecode("AbDh1D2h5DXh19D36h"))  # [1, -2, 4, -8, 16, -32, 64, -128, 256, -512]
```

### JavaScript

`js/dozencode.js` works as a browser script, an inline `<script>`, or a Node.js module.

**Browser / inline**

```html
<script src="dozencode.js"></script>
<script>
  console.log(dozencode([1, 10, 100, 1000]));   // AJ8D6YD
  console.log(dozdecode("AbDh1D2h5DXh19D36h")); // [1, -2, 4, -8, 16, -32, 64, -128, 256, -512]
</script>
```

**Node.js**

```js
const { dozencode, dozdecode } = require('./dozencode.js');
console.log(dozencode([1, 10, 100, 1000]));   // AJ8D6YD
console.log(dozdecode("AbDh1D2h5DXh19D36h")); // [1, -2, 4, -8, 16, -32, 64, -128, 256, -512]
```

An interactive test page is available at `js/test.html`.

## License

Dozencode is released to the public domain on May 23, 2024 by Colin M. Saunders.
