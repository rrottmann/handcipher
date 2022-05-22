import click
import handcipher.pad


@click.group()
def cli1():
    pass


@cli1.command()
@click.option('--key', prompt='Enter Password', help='The password for encryption.')
def create_pad(key: bytes):
    """Create a pad for manual encryption/decryption."""
    pad = handcipher.pad.create_pad(key=key.encode("utf-8"))
    handcipher.pad.pprint(pad)


@cli1.command()
@click.option('--key', prompt='Enter Password', help='The password for encryption.')
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def encrypt(key, input, output):
    """Encrypt input file using provided key and save it as output."""
    while True:
        chunk = input.read(1024)
        if not chunk:
            break
        encrypted_chunk = handcipher.pad.encrypt(s=chunk, key=key.encode("utf-8"))
        output.write(encrypted_chunk.encode("utf-8"))


@cli1.command()
@click.option('--key', prompt='Enter Password', help='The password for encryption.')
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def decrypt(key, input, output):
    """Decrypt input file using provided key and save it as output."""
    while True:
        encrypted_chunk = input.read(1024)
        if not encrypted_chunk:
            break
        chunk = handcipher.pad.decrypt(cipher_text=encrypted_chunk.decode("utf-8"), key=key.encode("utf-8"))
        output.write(chunk)


cli = click.CommandCollection(sources=[cli1])

if __name__ == '__main__':
    cli()
