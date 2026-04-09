/**
 * dozencode.js
 *
 * Dozencode: a duodecimal encoding for sequences of integers.
 * Encodes positive and negative integers without delimiters.
 *
 * Character set:
 *   Continuation digits (high-order): Z=0, A-K=1-11
 *   Terminal digit, positive ones:    0-9=0-9, j=10, k=11
 *   Terminal digit, negative ones:    z=-(n*12), y=-1..o=-11 (from high digits)
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
            encoded = String.fromCharCode(122 /* 'z' */ - remainder);
          } else if (remainder <= 9) {
            encoded = String.fromCharCode(48 /* '0' */ + remainder);
          } else {
            encoded = String.fromCharCode(97 /* 'a' */ + remainder - 1);
          }
        } else if (remainder === 0) {
          // Higher digit: zero
          encoded = 'Z' + encoded;
        } else {
          // Higher digit: 1-11
          encoded = String.fromCharCode(65 /* 'A' */ + remainder - 1) + encoded;
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

      if (ch >= '0' && ch <= '9') {
        // Positive terminal: 0-9
        var d = code - 48; /* '0' */
        number = (number === null) ? d : number * 12 + d;
        result.push(number);
        number = null;

      } else if (ch === 'j' || ch === 'k') {
        // Positive terminal: 10-11
        var d = code - 106 /* 'j' */ + 10;
        number = (number === null) ? d : number * 12 + d;
        result.push(number);
        number = null;

      } else if (ch === 'z') {
        // Negative terminal: -(n * 12), requires preceding continuation digits
        if (number === null) {
          throw new Error("unexpected 'z' in '" + encoded + "'; lone z must follow continuation digits");
        }
        result.push(-(number * 12));
        number = null;

      } else if (ch >= 'A' && ch <= 'K') {
        // Positive continuation digit: 1-11
        if (number === null) number = 0;
        number = number * 12 + (code - 65 /* 'A' */ + 1);

      } else if (ch === 'Z') {
        // Continuation digit: 0
        if (number === null) number = 0;
        number = number * 12;

      } else if (ch >= 'o' && ch <= 'y') {
        // Negative terminal: ones value 1-11
        var d = 121 /* 'y' */ - code + 1;
        number = (number === null) ? -d : -(number * 12 + d);
        result.push(number);
        number = null;

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
