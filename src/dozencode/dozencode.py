"""
dozencode.py
"""


import random
from typing import Callable


def dozdecoder(encoded: str, writer: Callable) -> int:
    """
    Doz-decode an encoded string into a list of integers
    """
    # pylint: disable=R0912
    written = 0
    integer = None
    negative = False
    for ch in encoded:
        if 'A' <= ch <= 'Z':
            if integer is not None:
                if negative:
                    integer = -integer
                    negative = False
                written += 1
                writer(integer)
                integer = None
            ch = ch.lower()
        if ch == 'z':
            if integer is None:
                integer = 0
            integer *= 12
        elif 'a' <= ch <= 'k':
            if integer is None:
                integer = 0
            integer *= 12
            integer += (ord(ch) - ord('a') + 1)
        elif 'o' <= ch <= 'y':
            if integer is None:
                integer = 0
            integer *= 12
            integer += (ord('y') - ord(ch) + 1)
            negative = True
        else:
            raise ValueError(f"unexpected ch '{ch}' in '{encoded}'")
    if integer is not None:
        if negative:
            integer = -integer
        written += 1
        writer(integer)
    return written


def dozencoder(integers: list, writer: Callable) -> int:
    """
    Doz-encode an iterator of integers
    """
    written = 0
    for integer in integers:
        negative = False
        if integer < 0:
            negative = True
            integer = -integer
        encoded = []
        while 1:
            remainder = integer % 12
            integer //= 12
            if integer == 0:
                if negative:
                    encoded.append(chr(ord('Z') - remainder))
                elif remainder == 0:
                    encoded.append('Z')
                else:
                    encoded.append(chr(ord('A') + remainder - 1))
                break
            elif remainder == 0:
                encoded.append('z')
            else:
                encoded.append(chr(ord('a') + remainder - 1))
        writer("".join(reversed(encoded)))
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
    for j in range(10):
        _ = j
        x = []
        for i in range(10):
            _ = i
            x.append(random.randint(-(1 << 16), (1 << 16)))
        test_list(x)
