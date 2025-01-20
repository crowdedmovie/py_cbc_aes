import os


def read_file_as_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        b_data: bytes = file.read()
    return b_data


def divide_into_blocks(b_data: bytes, block_size: int) -> list[bytes]:
    blocks: list[bytes] = [b_data[i:i + block_size] for i in range(0, len(b_data), block_size)]
    last_block_size: int = len(blocks[-1])

    if last_block_size < block_size:
        blocks[-1] = add_padding(blocks[-1], block_size)
    return blocks


def add_padding(block: bytes, block_size: int) -> bytes:
    padding_size: int = block_size - len(block)
    block += bytes([padding_size] * padding_size)
    return block


def remove_padding(block: bytes) -> bytes:
    # last byte => padding size
    padding_size: int = block[-1]

    if padding_size > len(block) or padding_size == 0:
        return None
    if block[-padding_size:] != bytes([padding_size] * padding_size):
        return None
    return block[:-padding_size]


def read_encrypted_data(file_path: str):
    with open(file_path, 'rb') as file:
        b_crypted_data: bytes = file.read()

    # Retrieves the block size, stored in the first byte
    block_size: int = b_crypted_data[0]

    # Retrieves the IV (the first 16 bytes after the block size)
    iv: bytes = b_crypted_data[1:17]

    # Splits the data into blocks of size block_size in a list
    blocks: list[bytes] = [b_crypted_data[i:i + block_size] for i in range(17, len(b_crypted_data), block_size)]

    return block_size, iv, blocks


def rot_word(word: bytes) -> bytes:
    return word[1:] + word[:1]

