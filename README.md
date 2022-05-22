# Handcipher

This cipher is designed so that it can be done on a piece of paper.

It is a substitution cipher with a pad that gets derived from a secret key:

1. Mix the alphabet based on the provided secret.
2. Create a matrix with 10 columns and fill in the mixed alphabet.
3. Transpose the matrix.

Encryption is done by locating the row and column of a character in the resulting matrix.
Thus, a single character is described by two numbers.

To encode arbitrary data, other characters need to be mapped on the alphabet.

## Manual Encryption

```
Enter Password: $%673dfhI
++++++++++++++++++++++++++++++++++++++++++
  : 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
0 : C | H | K | E | A | L | G | 9 | 6 | 3
1 : . | I | R | Y | 7 | M | S |   | D | P
2 : U | J | = | T | N | 1 | X | Q | 5 | O
3 : 8 | 0 | W | 2 | V | F | B | Z | 4
++++++++++++++++++++++++++++++++++++++++++
```

```
Cleartext: THIS IS A TEST
Ciphertext: 23 01 11 16 17 11 16 17 04 17 23 03 16 23
```

## Usage

```
$ python handcipher.py
Usage: handcipher.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create-pad  Create a pad for manual encryption/decryption.
  decrypt     Decrypt input file using provided key and save it as output.
  encrypt     Encrypt input file using provided key and save it as output.

$ python handcipher.py create-pad --help
Usage: handcipher.py create-pad [OPTIONS]

  Create a pad for manual encryption/decryption.

Options:
  --key TEXT  The password for encryption.
  --help      Show this message and exit.

$ python handcipher.py decrypt --help
Usage: handcipher.py decrypt [OPTIONS] INPUT OUTPUT

  Decrypt input file using provided key and save it as output.

Options:
  --key TEXT  The password for encryption.
  --help      Show this message and exit.

$ python handcipher.py encrypt --help
Usage: handcipher.py encrypt [OPTIONS] INPUT OUTPUT

  Encrypt input file using provided key and save it as output.

Options:
  --key TEXT  The password for encryption.
  --help      Show this message and exit.

```

### Example

> **Please Note:** The following example submits the key via commandline. This is insecure.
> If you omit `--key` parameter, you will be prompted for the key.
```bash
echo abc > test.txt
python handcipher.py encrypt test.txt test.txt.enc --key 12345678
python handcipher.py encrypt test.txt.enc test.txt.enc2 --key 12345678
python handcipher.py decrypt test.txt.enc2 test.txt.dec2 --key 12345678 
python handcipher.py decrypt test.txt.dec2 test.txt.dec --key 12345678 
echo ciphertext
cat test.txt.enc2
# 2721153034201717273506301320171227213530271806372731000000000000
echo original and decrypted cleartext
cat test.txt test.txt.dec
echo md5 hashes of original and decrypted cleartext
md5sum test.txt test.txt.dec
#0bee89b07a248e27c83fc3d5951213c1 *test.txt
#0bee89b07a248e27c83fc3d5951213c1 *test.txt.dec
```

## Security

This simple cipher of course is weak against modern cryptoanalysis.
As with every substitution cipher, it can be broken with frequency analysis.
So this cipher should be used multiple time to further scramble the text.

The cli only exposes the algorithm to encrypt arbitrary binary data.
The encoding increases mixing of the ciphertext and two rounds of encryption
should increase the robustness against frequency analysis.

There is the mantra in cryptography that you should not roll your own crypto.
This code has been created as an example to study why this is the case.

It was created so that it can be done using pen and paper. It is weak and should
only be used for learning purposes, escape room games and the like.
