"""
hozencode.py

Hozencode: base-16 variant of dozencode.

  Positive terminal (ones digit): Z=0, A-O=1-15
  Negative terminal (ones digit): z=-(n*16) [must follow continuations], a=-1..o=-15
  Continuation (high-order digits): 0-9=0-9, T=10, U=11, V=12, W=13, X=14, Y=15
"""


import random
from typing import Callable


def hozdecoder(encoded: str, writer: Callable) -> int:
    """
    Hoz-decode an encoded string into a list of integers.
    """
    written = 0
    number = None
    for ch in encoded:
        if ch == 'Z':
            # Positive terminal: value 0
            number = 0 if number is None else number * 16
            writer(number)
            number = None
            written += 1
        elif 'A' <= ch <= 'O':
            # Positive terminal: value 1-15
            r = ord(ch) - ord('A') + 1
            number = r if number is None else number * 16 + r
            writer(number)
            number = None
            written += 1
        elif ch == 'z':
            # Negative-zero terminal: must follow continuation digits
            if number is None:
                raise ValueError(f"unexpected 'z' in '{encoded}'; lone z must follow continuation digits")
            writer(-(number * 16))
            number = None
            written += 1
        elif 'a' <= ch <= 'o':
            # Negative terminal: value 1-15
            r = ord(ch) - ord('a') + 1
            number = -r if number is None else -(number * 16 + r)
            writer(number)
            number = None
            written += 1
        elif '0' <= ch <= '9':
            # Continuation: 0-9
            d = ord(ch) - ord('0')
            number = d if number is None else number * 16 + d
        elif 'T' <= ch <= 'Y':
            # Continuation: T=10, U=11, V=12, W=13, X=14, Y=15
            d = ord(ch) - ord('T') + 10
            number = d if number is None else number * 16 + d
        else:
            raise ValueError(f"unexpected ch '{ch}' in '{encoded}'")
    if number is not None:
        raise ValueError(f"unexpected end of stream in '{encoded}'")
    return written


def hozencoder(numbers: list, writer: Callable) -> int:
    """
    Hoz-encode an iterator of integers.
    """
    _CONT = '0123456789TUVWXY'
    written = 0
    for number in numbers:
        negative = False
        if number < 0:
            negative = True
            number = -number
        encoded = None
        while True:
            remainder = number % 16
            number //= 16
            if encoded is None:
                # Ones digit (terminal character)
                if negative:
                    encoded = 'z' if remainder == 0 else chr(ord('a') + remainder - 1)
                else:
                    encoded = 'Z' if remainder == 0 else chr(ord('A') + remainder - 1)
            else:
                # Higher-order digit (continuation character)
                encoded = _CONT[remainder] + encoded
            if number == 0:
                break
        writer(encoded)
        written += 1
    return written


def hozdecode(encoded: str) -> list:
    """
    Hoz-decode a string into a list of integers.
    """
    decoded = []
    hozdecoder(encoded, decoded.append)
    return decoded


def hozencode(integers: list) -> str:
    """
    Encode a list of integers into a hozencode string.
    """
    encoded = []
    hozencoder(integers, encoded.append)
    return ''.join(encoded)


def test_hozencode():
    """
    Test assertions for hozencode.
    """
    def test_list(integers):
        encoded = hozencode(integers)
        decoded = hozdecode(encoded)
        assert len(decoded) == len(integers), f"length mismatch for {integers}: got {decoded}"
        for idx, integer in enumerate(integers):
            assert integer == decoded[idx], f"mismatch at idx {idx}: {integer} != {decoded[idx]}"

    # Spot checks: positive terminals
    assert hozencode([0]) == 'Z',   hozencode([0])
    assert hozencode([1]) == 'A',   hozencode([1])
    assert hozencode([9]) == 'I',   hozencode([9])
    assert hozencode([10]) == 'J',  hozencode([10])
    assert hozencode([15]) == 'O',  hozencode([15])

    # Spot checks: continuations
    assert hozencode([16]) == '1Z',   hozencode([16])
    assert hozencode([17]) == '1A',   hozencode([17])
    assert hozencode([160]) == 'TZ',  hozencode([160])   # 10*16
    assert hozencode([176]) == 'UZ',  hozencode([176])   # 11*16
    assert hozencode([240]) == 'YZ',  hozencode([240])   # 15*16
    assert hozencode([256]) == '10Z', hozencode([256])   # 16^2

    # Spot checks: negative terminals
    assert hozencode([-1]) == 'a',    hozencode([-1])
    assert hozencode([-15]) == 'o',   hozencode([-15])
    assert hozencode([-16]) == '1z',  hozencode([-16])
    assert hozencode([-17]) == '1a',  hozencode([-17])
    assert hozencode([-160]) == 'Tz', hozencode([-160])
    assert hozencode([-256]) == '10z', hozencode([-256])

    # Decode spot checks
    assert hozdecode('Z') == [0]
    assert hozdecode('A') == [1]
    assert hozdecode('O') == [15]
    assert hozdecode('1Z') == [16]
    assert hozdecode('TZ') == [160]
    assert hozdecode('10Z') == [256]
    assert hozdecode('a') == [-1]
    assert hozdecode('o') == [-15]
    assert hozdecode('1z') == [-16]
    assert hozdecode('1a') == [-17]
    assert hozdecode('10z') == [-256]

    # Roundtrip: all integers in range
    for n in range(-300, 301):
        test_list([n])

    # Roundtrip: sequences
    test_list([])
    test_list([0])
    test_list([1, 2, 3])
    test_list([-1])
    test_list([-15])
    test_list([-16])
    test_list([-17])
    test_list([-100, -10, 0, 10, 100])

    # Random roundtrips
    for _ in range(1000):
        x = [random.randint(-(1 << 16), (1 << 16)) for _ in range(1000)]
        test_list(x)
