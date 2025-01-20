

def mix_columns(block: bytes, block_size: int, mix_type: str) -> bytes:
    # Converts the block into 4 sublists, each corresponding to one column
    columns: list[list[int]] = [list(block[i:i + 4]) for i in range(0, block_size, 4)]

    for i in range(len(columns)):
        if mix_type == "mix_collumns":
            columns[i] = mix_single_column(columns[i])
        if mix_type == "inv_mix_collumns":
            columns[i] = inverse_mix_single_column(columns[i])

    mixed_columns: bytes = bytes(sum(columns, []))
    return mixed_columns


def mix_single_column(column: list[int]) -> list[int]:
    """
    02 03 01 01
    01 02 03 01
    01 01 02 03
    03 01 01 02
    """
    a0: bytes
    a1: bytes
    a2: bytes
    a3: bytes
    a0, a1, a2, a3 = column

    # Calculate the new column by applying the multiplications in GF(2^8) according to the matrix above
    mixed_column: list[int] = [
        gf_multiply(a0, 2) ^ gf_multiply(a1, 3) ^ a2 ^ a3,  # 02 * a0 + 03 * a1 + a2 + a3
        a0 ^ gf_multiply(a1, 2) ^ gf_multiply(a2, 3) ^ a3,  # a0 + 02 * a1 + 03 * a2 + a3
        a0 ^ a1 ^ gf_multiply(a2, 2) ^ gf_multiply(a3, 3),  # a0 + a1 + 02 * a2 + 03 * a3
        gf_multiply(a0, 3) ^ a1 ^ a2 ^ gf_multiply(a3, 2)  # 03 * a0 + a1 + a2 + 02 * a3
    ]
    return mixed_column


def inverse_mix_single_column(column: list[int]) -> list[int]:
    """
    14 11 13 09
    09 14 11 13
    13 09 14 11
    11 13 09 14
    """
    a0: bytes
    a1: bytes
    a2: bytes
    a3: bytes
    a0, a1, a2, a3 = column

    # Calculate the new column by applying the multiplications in GF(2^8) according to the matrix above
    inv_mixed_column = [
        gf_multiply(a0, 14) ^ gf_multiply(a1, 11) ^ gf_multiply(a2, 13) ^ gf_multiply(a3, 9),
        gf_multiply(a0, 9) ^ gf_multiply(a1, 14) ^ gf_multiply(a2, 11) ^ gf_multiply(a3, 13),
        gf_multiply(a0, 13) ^ gf_multiply(a1, 9) ^ gf_multiply(a2, 14) ^ gf_multiply(a3, 11),
        gf_multiply(a0, 11) ^ gf_multiply(a1, 13) ^ gf_multiply(a2, 9) ^ gf_multiply(a3, 14)
    ]
    return inv_mixed_column


def gf_multiply(byte: bytes, multiplier_coef: int) -> bytes:
    # Multiplication by 14: (byte * 2) * 2 * 2 + (byte * 2) * 2 + (byte * 2)
    if multiplier_coef == 14:
        return gf_multiply(gf_multiply(gf_multiply(byte, 2), 2), 2) ^ gf_multiply(gf_multiply(byte, 2), 2) ^ gf_multiply(byte, 2)

    # Multiplication by 13: (byte * 2) * 2 * 2 + (byte * 2) * 2 + byte
    if multiplier_coef == 13:
        return gf_multiply(gf_multiply(gf_multiply(byte, 2), 2), 2) ^ gf_multiply(gf_multiply(byte, 2), 2) ^ byte

    # Multiplication by 11: (byte * 2) * 2 * 2 + (byte * 2) + byte
    if multiplier_coef == 11:
        return gf_multiply(gf_multiply(gf_multiply(byte, 2), 2), 2) ^ gf_multiply(byte, 2) ^ byte

    # Multiplication by 9: (byte * 2) * 2 * 2 + byte
    if multiplier_coef == 9:
        return gf_multiply(gf_multiply(gf_multiply(byte, 2), 2), 2) ^ byte

    # Multiplication by 3: (byte * 2) + byte
    if multiplier_coef == 3:
        return gf_multiply(byte, 2) ^ byte

    if multiplier_coef == 2:
        byte <<= 1
        if byte & 0x100:  # If the 9th bit is set (overflow of the 8-bit byte size)
            byte ^= 0x11B  # Reduce by the irreducible polynomial
        return byte

    # Multiplication by 1: Return the original byte without modification
    if multiplier_coef == 1:
        return byte

