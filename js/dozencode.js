/**
 * dozencode.js
 *
 * Dozencode: a duodecimal encoding for sequences of integers.
 * Encodes positive and negative integers without delimiters.
 *
 * Character set:
 *   Positive terminal (ones digit): Z=0, A-K=1-11
 *   Negative terminal (ones digit): z=-(n*12) [must follow continuations], a=-1..k=-11
 *   Continuation (high-order digits): 0-9=0-9, X=10, Y=11
 *
 * Released to the public domain by Colin M. Saunders, May 23 2024.
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = factory();
  } else {
    var exp = factory();
    root.dozencode = exp.dozencode;
    root.dozdecode = exp.dozdecode;
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {

  /**
   * Encode an array of integers into a dozencode string.
   * @param {number[]} numbers
   * @returns {string}
   */
  function dozencode(numbers) {
    var parts = [];
    for (var i = 0; i < numbers.length; i++) {
      var num = numbers[i];
      var negative = false;
      if (num < 0) {
        negative = true;
        num = -num;
      }
      var encoded = null;
      while (true) {
        var remainder = num % 12;
        num = Math.floor(num / 12);
        if (encoded === null) {
          // Ones digit (terminal character)
          if (negative) {
            encoded = remainder === 0 ? 'z' : String.fromCharCode(97 /* 'a' */ + remainder - 1);
          } else {
            encoded = remainder === 0 ? 'Z' : String.fromCharCode(65 /* 'A' */ + remainder - 1);
          }
        } else {
          // Higher-order digit (continuation character)
          if (remainder <= 9) {
            encoded = String.fromCharCode(48 /* '0' */ + remainder) + encoded;
          } else if (remainder === 10) {
            encoded = 'X' + encoded;
          } else {
            encoded = 'Y' + encoded;
          }
        }
        if (num === 0) break;
      }
      parts.push(encoded);
    }
    return parts.join('');
  }

  /**
   * Decode a dozencode string into an array of integers.
   * @param {string} encoded
   * @returns {number[]}
   */
  function dozdecode(encoded) {
    var result = [];
    var number = null;

    for (var i = 0; i < encoded.length; i++) {
      var ch = encoded[i];
      var code = encoded.charCodeAt(i);

      if (ch === 'Z') {
        // Positive terminal: value 0
        result.push(number === null ? 0 : number * 12);
        number = null;

      } else if (ch >= 'A' && ch <= 'K') {
        // Positive terminal: value 1-11
        var r = code - 64; /* code - 'A' + 1 */
        result.push(number === null ? r : number * 12 + r);
        number = null;

      } else if (ch === 'z') {
        // Negative-zero terminal: must follow continuation digits
        if (number === null) {
          throw new Error("unexpected 'z' in '" + encoded + "'; lone z must follow continuation digits");
        }
        result.push(-(number * 12));
        number = null;

      } else if (ch >= 'a' && ch <= 'k') {
        // Negative terminal: value 1-11
        var r = code - 96; /* 'a' - 1 + 1 = code - 'a' + 1 */
        result.push(number === null ? -r : -(number * 12 + r));
        number = null;

      } else if (ch >= '0' && ch <= '9') {
        // Continuation: 0-9
        var d = code - 48; /* '0' */
        number = number === null ? d : number * 12 + d;

      } else if (ch === 'X') {
        // Continuation: 10
        number = number === null ? 10 : number * 12 + 10;

      } else if (ch === 'Y') {
        // Continuation: 11
        number = number === null ? 11 : number * 12 + 11;

      } else {
        throw new Error("unexpected character '" + ch + "' in '" + encoded + "'");
      }
    }

    if (number !== null) {
      throw new Error("unexpected end of stream in '" + encoded + "'");
    }

    return result;
  }

  return { dozencode: dozencode, dozdecode: dozdecode };
});
