import unittest
import string

from handcipher.pad import create_pad, encrypt, encrypt_b32, decrypt_chr, decrypt_raw, decrypt


class MyTestCase(unittest.TestCase):
    def test_pad_generation(self):
        key = b"test"
        pad = create_pad(key=key)
        expected_pad = {0: ['6', ' ', 'E', '.', '3', '0', 'T', 'Y', 'Q', 'W'],
                        1: ['7', 'Z', 'O', 'L', 'D', 'J', 'A', 'H', 'S', 'K'],
                        2: ['9', '4', 'P', '1', 'I', 'V', 'B', 'X', 'C', '5'],
                        3: ['F', 'U', '2', 'M', 'N', 'G', '=', '8', 'R']}
        self.assertEqual(pad, expected_pad)
        key = b"another"
        pad = create_pad(key=key)
        expected_pad = {0: ['G', 'F', 'N', '2', '9', 'T', 'L', 'R', 'Z', '='],
                        1: ['D', ' ', '1', '5', 'B', 'A', 'M', '8', 'J', 'U'],
                        2: ['H', 'Q', '3', 'K', 'Y', 'P', '6', 'C', 'W', 'V'],
                        3: ['E', '4', 'X', 'I', '7', '0', 'O', 'S', '.']}
        self.assertEqual(pad, expected_pad)

    def test_encrypt(self):
        key = b"test"
        s = "© 2022 by Reiner Rottmann".encode("utf-8")
        ciphertext = encrypt(key=key, s=s)
        expected_ciphertext = '071931181633380835241128160706110226153519321312332511281631062212383235320713123407363636363636'
        self.assertEqual(ciphertext, expected_ciphertext)

    def test_encrypt_b32(self):
        key = b"test"
        alphabet = list(string.ascii_uppercase + string.digits + "= .")
        b32 = "© 2022 by Reiner Rottmann".upper()
        b32_cleansed = ""
        for _ in b32:
            if not _ in alphabet:
                continue
            b32_cleansed = b32_cleansed + _
        ciphertext = encrypt_b32(b32=b32_cleansed, key=key)
        expected_ciphertext = '013205323201260701380224340238013812060633163434'
        self.assertEqual(ciphertext, expected_ciphertext)

    def test_decrypt_chr(self):
        key = b"test"
        pad = create_pad(key=key)
        two_chars = "38"
        decrypted_chr = decrypt_chr(two_chars=two_chars, pad=pad)
        expected_decrypted_chr = "R"
        self.assertEqual(decrypted_chr, expected_decrypted_chr)

    def test_decrypt_raw(self):
        key = b"test"
        pad = create_pad(key=key)
        cipher_text = '013205323201260701380224340238013812060633163434'
        clear_text_raw = decrypt_raw(cipher_text=cipher_text, pad=pad)
        expected_clear_text_raw = ' 2022 BY REINER ROTTMANN'
        self.assertEqual(clear_text_raw, expected_clear_text_raw)

    def test_decrypt(self):
        key = b"test"
        s = "© 2022 by Reiner Rottmann".encode("utf-8")
        cipher_text = encrypt(key=key, s=s)
        decrypted = decrypt(cipher_text=cipher_text, key=key)
        self.assertEqual(decrypted, s)





if __name__ == '__main__':
    unittest.main()
