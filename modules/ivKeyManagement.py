import os
import random


def generate_iv(size: int) -> bytes:
    return random.randbytes(size)


def generate_key(size: int, file_path: str):
    key = random.randbytes(size)

    input_file_name: str = os.path.splitext(file_path)[0]
    key_file_name: str = f"{input_file_name}_key.bin"

    with open(key_file_name, "wb") as file:
        file.write(key)
    return key, key_file_name


def read_key(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        key = file.read()
    return key
