def base36encode(number, alphabet="0123456789abcdefghijklmnopqrstuvwxyz"):
    base36 = ""
    if 0 <= number < len(alphabet):
        return alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return base36


def base36decode(number):
    return int(number, 36)


string = "www.google.comé"
string = string.encode()
foo = int.from_bytes(string)
foo = base36encode(foo)
print(foo)

bar = base36decode(foo)
bar = bar.to_bytes((bar.bit_length() + 7) // 8, byteorder="big").decode()
print(bar)
