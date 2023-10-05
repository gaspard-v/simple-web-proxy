function bytesToInt(bytes) {
    let result = 0n;
    for (let i = 0; i < bytes.length; i++) {
        result = (result << 8n) | BigInt(bytes[i]);
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

function intToStr(number, encoding = "utf-8") {
    function splitBigIntIntoBytes(bigIntValue) {
        if (!BigInt(bigIntValue)) {
            throw new Error("La valeur doit être un BigInt.");
        }

        if (bigIntValue < 0n) {
            throw new Error("La valeur doit être un BigInt positif.");
        }

        const byteArray = [];

        while (bigIntValue > 0n) {
            const byte = BigInt(bigIntValue) & BigInt(0xff);
            byteArray.unshift(Number(byte)); // Utiliser unshift pour ajouter les octets dans l'ordre correct
            bigIntValue >>= 8n; // Décaler de 8 bits vers la droite pour traiter le prochain octet
        }

        return byteArray;
    }
    const intArray = splitBigIntIntoBytes(number);
    let utf8String = "";
    for (let i = 0; i < intArray.length; i++) {
        const intValue = intArray[i];

        // Vérifier si la valeur est un entier
        if (typeof intValue !== "number" || intValue % 1 !== 0) {
            throw new Error("La valeur doit être un entier.");
        }

        // Vérifier si la valeur est dans la plage valide pour un caractère UTF-8
        if (intValue < 0 || intValue > 0x10ffff) {
            throw new Error(
                "La valeur est hors de la plage valide pour un caractère UTF-8.",
            );
        }

        if (intValue <= 0x7f) {
            // Pour les caractères ASCII (0-127), un seul octet suffit
            utf8String += String.fromCharCode(intValue);
        } else if (intValue <= 0x7ff) {
            // Pour les caractères dans la plage 128-2047, nous avons besoin de deux octets
            const byte1 = 0xc0 | ((intValue >> 6) & 0x1f);
            const byte2 = 0x80 | (intValue & 0x3f);
            utf8String += String.fromCharCode(byte1, byte2);
        } else if (intValue <= 0xffff) {
            // Pour les caractères dans la plage 2048-65535, nous avons besoin de trois octets
            const byte1 = 0xe0 | ((intValue >> 12) & 0x0f);
            const byte2 = 0x80 | ((intValue >> 6) & 0x3f);
            const byte3 = 0x80 | (intValue & 0x3f);
            utf8String += String.fromCharCode(byte1, byte2, byte3);
        } else {
            // Pour les caractères dans la plage 65536-1114111, nous avons besoin de quatre octets
            const byte1 = 0xf0 | ((intValue >> 18) & 0x07);
            const byte2 = 0x80 | ((intValue >> 12) & 0x3f);
            const byte3 = 0x80 | ((intValue >> 6) & 0x3f);
            const byte4 = 0x80 | (intValue & 0x3f);
            utf8String += String.fromCharCode(byte1, byte2, byte3, byte4);
        }
    }
    return utf8String;
}

function numberEncode(number, alphabet) {
    let baseX = "";
    const alphabetLength = BigInt(alphabet.length);
    if (0n <= number && number < alphabetLength) {
        return alphabet[number];
    }
    while (number !== 0n) {
        const remainder = number % alphabetLength;
        number = number / alphabetLength;
        baseX = alphabet[Number(remainder)] + baseX;
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
    } else if (Buffer.isBuffer(element)) {
        element = bytesToInt(element);
    } else if (typeof element !== "number") {
        throw new TypeError("element must be a string, number, or Buffer");
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

export function test() {
    const string = "I am a test &é*µù$^^";
    const foo = encode(string);
    console.log(foo);
    const bar = decode(foo);
    console.log(bar);
}
