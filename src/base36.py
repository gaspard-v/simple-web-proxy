def __bytes_to_int(bytes: bytes) -> int:
    return int.from_bytes(bytes, byteorder="big")


def __str_to_bytes(string: str, *args, **kwargs) -> bytes:
    return string.encode(*args, **kwargs)


def __str_to_int(string: str, *, encoding: str = "utf-8") -> int:
    bytes = __str_to_bytes(string, encoding=encoding)
    return __bytes_to_int(bytes)


def __int_to_bytes(number: int) -> bytes:
    number_bytes = (number.bit_length() + 7) // 8
    return number.to_bytes(number_bytes, byteorder="big")


def __bytes_to_str(bytes: bytes, *args, **kwargs) -> str:
    return bytes.decode(*args, **kwargs)


def __int_to_str(number: int, *, encoding: str = "utf-8") -> str:
    bytes = __int_to_bytes(number)
    return __bytes_to_str(bytes, encoding=encoding)


def __number_encode(number: int, alphabet: str) -> str:
    baseX = ""
    if 0 <= number < len(alphabet):
        return alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        baseX = alphabet[i] + baseX
    return baseX


def __number_decode(number: str | bytes | bytearray, base: int) -> int:
    return int(number, base)


def encode(
    element: str | int | bytes,
    *,
    alphabet: str = "0123456789abcdefghijklmnopqrstuvwxyz",
    encoding: str = "utf-8"
) -> str:
    if type(element) is str:
        element = __str_to_int(element, encoding=encoding)
    elif type(element) is bytes:
        element = __bytes_to_int(element)
    elif type(element) is not int:
        raise TypeError('"element" must be and str, int or bytes')
    return __number_encode(element, alphabet)


def decode(
    element: str | bytes | bytearray,
    *,
    alphabet: str = "0123456789abcdefghijklmnopqrstuvwxyz",
    encoding: str = "utf-8"
) -> str:
    number = __number_decode(element, len(alphabet))
    return __int_to_str(number, encoding=encoding)


def __test():
    string = "I am a test &é*µù$^^"
    foo = encode(string)
    print(foo)
    bar = decode(foo)
    print(bar)


__test()
