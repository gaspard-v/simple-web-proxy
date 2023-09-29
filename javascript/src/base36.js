function bytesToInt(bytes) {
    let result = 0;
    for (let i = 0; i < bytes.length; i++) {
        result = result * 256 + bytes[i];
    }
    return result;
}

function strToBytes(string, encoding = "utf-8") {
    const encoder = new TextEncoder(encoding);
    return encoder.encode(string);
}

function strToInt(string, encoding = "utf-8") {
    const bytes = strToBytes(string, encoding);
    return bytesToInt(bytes);
}

function intToBytes(number) {
    const bytes = [];
    while (number > 0) {
        bytes.unshift(number & 0xff);
        number >>= 8;
    }
    return new Uint8Array(bytes);
}

function bytesToStr(bytes, encoding = "utf-8") {
    const decoder = new TextDecoder(encoding);
    return decoder.decode(bytes);
}

function intToStr(number, encoding = "utf-8") {
    const bytes = intToBytes(number);
    return bytesToStr(bytes, encoding);
}

function numberEncode(number, alphabet) {
    let baseX = "";
    if (0 <= number && number < alphabet.length) {
        return alphabet[number];
    }

    while (number !== 0) {
        const remainder = number % alphabet.length;
        number = Math.floor(number / alphabet.length);
        baseX = alphabet.charAt(remainder) + baseX;
    }
    return baseX;
}

function numberDecode(number, base) {
    return parseInt(number, base);
}

export function encode(
    element,
    {
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz",
        encoding = "utf-8",
    } = {},
) {
    if (typeof element === "string") {
        element = strToInt(element, encoding);
    } else if (element instanceof Uint8Array) {
        element = bytesToInt(element);
    } else if (typeof element !== "number") {
        throw new TypeError(
            '"element" must be a string, number, or Uint8Array',
        );
    }
    return numberEncode(element, alphabet);
}

export function decode(
    element,
    {
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz",
        encoding = "utf-8",
    } = {},
) {
    const number = numberDecode(element, alphabet.length);
    return intToStr(number, encoding);
}
