from modules import DataPreparation, ivKeyManagement, cbcOperations, outputFileOperation


def encrypt_file(input_file_path: str, output_file_path: str, key_size: int, block_size: int) -> None:
    print("Encrypting the file...")

    # Reading the file to encrypt in binary
    b_data: bytes = DataPreparation.read_file_as_bytes(input_file_path)

    # Dividing the data into blocks of the specified size
    blocks: list[bytes] = DataPreparation.divide_into_blocks(b_data, block_size)

    # Generating the initialization vector (IV) of the block size
    iv: bytes = ivKeyManagement.generate_iv(block_size)

    # Generating and saving the key in a file named based on the output file name
    key_info: tuple[bytes, str] = ivKeyManagement.generate_key(key_size, output_file_path)
    key: bytes = key_info[0]
    key_file_name: str = key_info[1]

    # Encrypting the blocks using the IV and the key
    encrypted_blocks: list[bytes] = cbcOperations.encrypt_blocks(blocks, iv, key, block_size)

    # Saving the encrypted file, including the IV and block size
    outputFileOperation.save_encrypted_file(output_file_path, iv, encrypted_blocks, block_size)

    print(f"The following encrypted file was created: {output_file_path}")
    print(f"The following key file was created: {key_file_name}")


def decrypt_file(input_file_path: str, output_file_path: str, key_file_path: str) -> None:
    if key_file_path is None:
        print("ERROR: Missing decryption key file. Specify it using the -k argument.")
        return

    print("Decrypting the file...")

    # Extracting the block size, IV, and encrypted blocks from the file
    data_info: tuple[int, bytes, list[bytes]] = DataPreparation.read_encrypted_data(input_file_path)
    block_size: int = data_info[0]
    iv: bytes = data_info[1]
    encrypted_blocks: list[bytes] = data_info[2]

    # Reading the decryption key from the specified file
    key: bytes = ivKeyManagement.read_key(key_file_path)

    # Decrypting the blocks using the IV and the key
    decrypted_blocks: list[bytes] = cbcOperations.decrypt_blocks(encrypted_blocks, iv, key, block_size)

    # Saving the decrypted blocks to the output file
    outputFileOperation.save_decrypted_file(output_file_path, decrypted_blocks)

    print(f"The following decrypted file was created: {output_file_path}")


