from modules.aes import KeySchedule, MixColumns, ShiftRows, SubBytes
from modules import cbcOperations


def aes_encrypt(block: bytes, block_size: int, key: bytes) -> bytes:
    key_size: int = len(key)

    # Configuring parameters based on the key size
    # main_rounds => number of rounds based on the key size
    # round_keys_indicie_mod => index of the round key for the first iteration of the main rounds
    if key_size == 16:
        main_rounds: int = 9
        round_keys_indicie_mod: int = 0
    if key_size == 24:
        main_rounds: int = 11
        round_keys_indicie_mod: int = 1
    if key_size == 32:
        main_rounds: int = 13
        round_keys_indicie_mod: int = 1

    # Generate the round keys from the main key
    rounds_keys: list[bytes] = KeySchedule.key_schedule(key, key_size)

    # Initial round
    if key_size == 16:
        block = cbcOperations.xor(block, key, block_size)
    if key_size == 24 or key_size == 32:
        block = cbcOperations.xor(block, rounds_keys[0], block_size)

    # Main rounds
    for i in range(main_rounds):
        block = SubBytes.subbytes_operations(block, "s_box")
        block = ShiftRows.shift_rows(block, block_size, "shift")
        block = MixColumns.mix_columns(block, block_size, "mix_collumns")
        block = cbcOperations.xor(block, rounds_keys[i + round_keys_indicie_mod], block_size)

    # Final round
    block = SubBytes.subbytes_operations(block, "s_box")
    block = ShiftRows.shift_rows(block, block_size, "shift")
    encrypted_block: bytes = cbcOperations.xor(block, rounds_keys[-1], block_size)

    return encrypted_block


def aes_decrypt(block: bytes, block_size: int, key: bytes) -> bytes:
    key_size: int = len(key)

    # Configuring parameters based on the key size
    # main_rounds => number of rounds based on the key size
    # round_keys_indicie_mod => index of the round key for the first iteration of the main rounds
    if key_size == 16:
        main_rounds: int = 9
        round_keys_indicie_mod: int = 0
    if key_size == 24:
        main_rounds: int = 11
        round_keys_indicie_mod: int = 1
    if key_size == 32:
        main_rounds: int = 13
        round_keys_indicie_mod: int = 1

    # Generate the round keys from the main key
    rounds_keys: list[bytes] = KeySchedule.key_schedule(key, key_size)

    # Final round
    block = cbcOperations.xor(block, rounds_keys[-1], block_size)
    block = ShiftRows.shift_rows(block, block_size, "inv_shift")
    block = SubBytes.subbytes_operations(block, "inv_s_box")

    # Main rounds
    for i in range(main_rounds - 1, -1, -1):
        block = cbcOperations.xor(block, rounds_keys[i + round_keys_indicie_mod], block_size)
        block = MixColumns.mix_columns(block, block_size, "inv_mix_collumns")
        block = ShiftRows.shift_rows(block, block_size, "inv_shift")
        block = SubBytes.subbytes_operations(block, "inv_s_box")

    # Initial round
    if key_size == 16:
        decrypted_block: bytes = cbcOperations.xor(block, key, block_size)
    if key_size == 24 or key_size == 32:
        decrypted_block: bytes = cbcOperations.xor(block, rounds_keys[0], block_size)

    return decrypted_block



