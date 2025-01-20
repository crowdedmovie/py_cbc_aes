from modules import DataPreparation
from modules.aes import aesOperations

def xor(block1: bytes | list[bytes], block2: bytes | list[bytes], block_size: int) -> bytes:
    # Checks if the blocks are in the list of bytes format, if so, converts them to bytes
    if isinstance(block1, list) and all(isinstance(b, bytes) for b in block1):
        block1 = b''.join(block1)
    if isinstance(block2, list) and all(isinstance(b, bytes) for b in block2):
        block2 = b''.join(block2)

    return bytes(block1[i] ^ block2[i] for i in range(block_size))


def encrypt_blocks(blocks: list[bytes], iv: bytes, key: bytes, block_size: int) -> list[bytes]:
    encrypted_blocks: list[bytes] = []

    # Encrypt the first block using the IV and the key
    first_block: bytes = xor(blocks[0], iv, block_size)
    encrypted_first_block: bytes = xor(first_block, key, block_size)
    encrypted_blocks.append(encrypted_first_block)

    # Encrypt the following blocks using the previously encrypted block and the key
    for i in range(1, len(blocks)):
        current_block: bytes = xor(blocks[i], encrypted_blocks[i - 1], block_size)
        encrypted_current_block: bytes = aesOperations.aes_encrypt(current_block, block_size, key)
        encrypted_blocks.append(encrypted_current_block)
    return encrypted_blocks


def decrypt_blocks(encrypted_blocks: list[bytes], iv: bytes, key: bytes, block_size: int) -> list[bytes]:
    decrypted_blocks = [None] * len(encrypted_blocks)

    # Decrypt starting from the last block
    for i in range(len(encrypted_blocks) - 1, 0, -1):
        current_block: bytes = aesOperations.aes_decrypt(encrypted_blocks[i], block_size, key)
        decrypted_blocks[i] = xor(current_block, encrypted_blocks[i - 1], block_size)

    # Decrypt the first block separately with the key and then the IV
    decrypted_blocks[0] = xor(encrypted_blocks[0], key, block_size)
    decrypted_blocks[0] = xor(decrypted_blocks[0], iv, block_size)
    decrypted_blocks[-1] = DataPreparation.remove_padding(decrypted_blocks[-1])

    return decrypted_blocks
