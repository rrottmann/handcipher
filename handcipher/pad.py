import string
import base64
import binascii


def pprint(pad: dict):
    """Pretty print a pad."""
    max_i = 0
    for _ in pad:
        i = len(pad[_])
        if i > max_i:
            max_i = i
    print("+" * ((i + 1) * 4 + 2))
    print("  : " + " | ".join([str(x) for x in range(0, max_i)]))
    for _ in pad:
        print(f"{_} : {' | '.join(pad[_])}")
    #print("  : " + " | ".join([str(x) for x in range(0, max_i)]))
    print("+" * ((i + 1) * 4 + 2))


def create_pad(key: bytes = b"secret", max_columns: int = 10, alphabet: str = None) -> dict:
    """
    Derive a pad from the given key that is later used to encrypt and decrypt.
    First the alphabet gets shuffled and then columns are transposed.
    """
    # create alphabet
    if alphabet is None:
        alphabet = list(string.ascii_uppercase + string.digits + "= .")
    # permutate alphabet
    keyhex = binascii.hexlify(key)
    permutated_alphabet = list()
    pos_alphabet = 0
    pos_keyhex = 0
    while alphabet:
        try:
            key_char = keyhex.decode("utf-8")[pos_keyhex]
        except IndexError:
            pos_keyhex = 0
            key_char = keyhex.decode("utf-8")[pos_keyhex]
        # how many positions to move?
        move = int(key_char, 16)
        # odd: move left; even: move right
        if move % 2 == 0:
            direction = 1
        else:
            direction = -1
        while move > 0:
            if direction > 0:
                pos_alphabet += 1
                if pos_alphabet > len(alphabet):
                    pos_alphabet = 0
            else:
                pos_alphabet -= 1
                if pos_alphabet < 0:
                    pos_alphabet = len(alphabet) - 1
            move -= 1
        try:
            permutated_alphabet.append(alphabet[pos_alphabet % len(alphabet)])
        except IndexError:
            # this should not happen
            pass
        try:
            del alphabet[pos_alphabet % len(alphabet)]
        except IndexError:
            # this should not happen
            pass
        pos_keyhex += 1
    # create empty pad
    tmp_pad = dict()
    for _ in range(0, max_columns):
        tmp_pad[_] = []
    # fill pad
    for _, char in enumerate(permutated_alphabet):
        i = _ % max_columns
        tmp_pad[i].append(char)
    # read columns
    pad = dict()
    i = 0
    while True:
        pad[i] = list()
        _ = None
        for j in tmp_pad.keys():
            try:
                _ = tmp_pad[j][i]
            except IndexError:
                pass
            if _:
                if not _ in pad[i]:
                    pad[i].append(_)
        if not _:
            if not pad[i]:
                del pad[i]
            break
        else:
            i += 1
    return pad


def encrypt(s: bytes, key: bytes) -> str:
    """
    Encrypt arbitrary bytes by base32 encoding it first.
    Results in a string containing row and column locations of the origin char (bipartit).
    """
    b32 = base64.b32encode(s).decode("utf-8")
    encrypted = encrypt_b32(b32=b32, key=key)
    return encrypted


def encrypt_b32(b32: str, key: bytes) -> str:
    """
    Encrypt a string that only has base32 safe characters.
    Results in a string containing row and column locations of the origin char (bipartit).
    """
    pad = create_pad(key=key)
    encrypted = []
    for _ in b32:
        e = encrypt_chr(c=_, pad=pad)
        encrypted.append(e)
    return "".join(encrypted)


def encrypt_chr(c: str, pad: dict) -> str:
    """Transpose char c with row and column of pad location."""
    e = ""
    for _ in pad:
        if c in pad[_]:
            e = f"{_}{pad[_].index(c)}"
    if not e:
        raise Exception("Encryption Error")
    return "".join(e)


def decrypt(cipher_text: str, key: bytes) -> bytes:
    pad = create_pad(key=key)
    decrypted_raw = decrypt_raw(cipher_text=cipher_text, pad=pad)
    decrypted = base64.b32decode(decrypted_raw)
    return decrypted


def decrypt_raw(cipher_text: str, pad: dict) -> str:
    """Decrypt a cipher_text to a raw clear text."""
    _ = 0
    decrypted_raw = ""
    while True:
        two_chars = cipher_text[_:_ + 2]
        if not two_chars:
            break
        decrypted_chr = decrypt_chr(two_chars=two_chars, pad=pad)
        decrypted_raw = decrypted_raw + decrypted_chr
        _ += 2
        if _ > len(cipher_text):
            break
    return decrypted_raw


def decrypt_chr(two_chars: str, pad: dict) -> str:
    """Decrypt two_chars that resemble a location on the pad and return single char."""
    decrypted_chr = None
    try:
        decrypted_chr = pad[int(two_chars[0])][int(two_chars[1])]
    except KeyError:
        pass
    return decrypted_chr
