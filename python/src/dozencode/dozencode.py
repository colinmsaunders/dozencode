"""
dozencode.py

Character set:
  Positive terminal (ones digit): Z=0, A-K=1-11
  Negative terminal (ones digit): z=-(n*12) [must follow continuations], a=-1..k=-11
  Continuation (high-order digits): 0-9=0-9, X=10, Y=11
"""


import random
from typing import Callable


def dozdecoder(encoded: str, writer: Callable) -> int:
    """
    Doz-decode an encoded string into a list of integers
    """
    written = 0
    number = None
    for ch in encoded:
        if ch == 'Z':
            # Positive terminal: value 0
            number = 0 if number is None else number * 12
            writer(number)
            number = None
            written += 1
        elif 'A' <= ch <= 'K':
            # Positive terminal: value 1-11
            r = ord(ch) - ord('A') + 1
            number = r if number is None else number * 12 + r
            writer(number)
            number = None
            written += 1
        elif ch == 'z':
            # Negative-zero terminal: must follow continuation digits
            if number is None:
                raise ValueError(f"unexpected 'z' in '{encoded}'; lone z must follow continuation digits")
            writer(-(number * 12))
            number = None
            written += 1
        elif 'a' <= ch <= 'k':
            # Negative terminal: value 1-11
            r = ord(ch) - ord('a') + 1
            number = -r if number is None else -(number * 12 + r)
            writer(number)
            number = None
            written += 1
        elif '0' <= ch <= '9':
            # Continuation: 0-9
            d = ord(ch) - ord('0')
            number = d if number is None else number * 12 + d
        elif ch == 'X':
            # Continuation: 10
            number = 10 if number is None else number * 12 + 10
        elif ch == 'Y':
            # Continuation: 11
            number = 11 if number is None else number * 12 + 11
        else:
            raise ValueError(f"unexpected ch '{ch}' in '{encoded}'")
    if number is not None:
        raise ValueError(f"unexpected end of stream in '{encoded}'")
    return written


def dozencoder(numbers: list, writer: Callable) -> int:
    """
    Doz-encode an iterator of integers
    """
    written = 0
    for number in numbers:
        negative = False
        if number < 0:
            negative = True
            number = -number
        encoded = None
        while 1:
            remainder = number % 12
            number //= 12
            if encoded is None:
                # Ones digit (terminal character)
                if negative:
                    encoded = 'z' if remainder == 0 else chr(ord('a') + remainder - 1)
                else:
                    encoded = 'Z' if remainder == 0 else chr(ord('A') + remainder - 1)
            else:
                # Higher-order digit (continuation character)
                if remainder <= 9:
                    encoded = chr(ord('0') + remainder) + encoded
                elif remainder == 10:
                    encoded = 'X' + encoded
                else:
                    encoded = 'Y' + encoded
            if number == 0:
                break
        writer(encoded)
        written += 1
    return written


def dozdecode(encoded: str) -> list:
    """
    Doz-decode a string into a list of integers
    """
    decoded = []
    dozdecoder(encoded, decoded.append)
    return decoded


def dozencode(integers: list) -> str:
    """
    Encode a list of integers into a string
    """
    encoded = []
    dozencoder(integers, encoded.append)
    return ''.join(encoded)


def test_dozencode():
    """
    Some test assertions
    """

    def test_list(integers):
        """
        Encode then decode
        """
        encoded = dozencode(integers)
        decoded = dozdecode(encoded)
        assert len(decoded) == len(integers)
        for idx, integer in enumerate(integers):
            assert integer == decoded[idx]

    test_list([])
    test_list([0,])
    test_list([1,])
    test_list([2,])
    test_list([3,])
    test_list([4,])
    test_list([5,])
    test_list([6,])
    test_list([7,])
    test_list([8,])
    test_list([9,])
    test_list([10,])
    test_list([11,])
    test_list([12,])
    test_list([1, 2, 3])
    test_list([-1,])
    test_list([-20,])
    test_list([-15,])
    test_list([-16,])
    test_list([-17,])
    test_list([-100, -10, 0, 10, 100])
    for j in range(1000):
        _ = j
        x = []
        for i in range(1000):
            _ = i
            x.append(random.randint(-(1 << 16), (1 << 16)))
        test_list(x)
