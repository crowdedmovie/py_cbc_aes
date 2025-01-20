def save_encrypted_file(file_path: str, iv: bytes, encrypted_blocks: list[bytes], block_size: int) -> None:
    with open(file_path, 'wb') as file:
        file.write(bytes([block_size]))
        file.write(iv)
        for block in encrypted_blocks:
            file.write(block)


def save_decrypted_file(file_path: str, decrypted_blocks: list[bytes]) -> None:
    with open(file_path, 'wb') as file:
        for block in decrypted_blocks:
            file.write(block)
