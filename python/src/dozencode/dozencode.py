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
    number = None
    negative = False
    for ch in encoded:
        if '0' <= ch <= '9':
            if number is None:
                number = ord(ch) - ord('0')
            else:
                number = (number * 12) + (ord(ch) - ord('0'))
            written += 1
            writer(number)
            number = None
        elif 'j' <= ch <= 'k':
            if number is None:
                number = ord(ch) - ord('j') + 10
            else:
                number = (number * 12) + (ord(ch) - ord('j') + 10)
            written += 1
            writer(number)
            number = None
        elif ch == 'z':
            if number is None:
                raise ValueError(f"unexpected ch '{ch}' in '{encoded}'; lone z must be at the end of an string")      
            number = -1 * (number * 12)
            written += 1
            writer(number)
            number = None
        elif 'A' <= ch <= 'K':
            if number is None:
                number = 0
            number *= 12
            number += (ord(ch) - ord('A') + 1)
        elif ch == 'Z':
            if number is None:
                number = 0
            number *= 12
        elif 'o' <= ch <= 'y':
            if number is None:
                number = -1 * (ord('y') - ord(ch) + 1)
            else:
                number = -1 * ((number * 12) + (ord('y') - ord(ch) + 1))
            written += 1
            writer(number)
            number = None
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
                if negative:
                    encoded = chr(ord('z') - remainder)
                elif remainder <= 9:
                    encoded = chr(ord('0') + remainder)
                else:
                    encoded = chr(ord('a') + (remainder - 1))
            elif remainder == 0:
                encoded = 'Z' + encoded
            else:
                encoded = chr(ord('A') + remainder - 1) + encoded
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
