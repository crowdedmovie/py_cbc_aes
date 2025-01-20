def shift_rows(block: bytes, block_size: int, shift_type: str) -> bytes:
    rows: list[list[int]] = [list(block[i:i + 4]) for i in range(0, block_size, 4)]

    # Determines the shift direction based on the shift type
    if shift_type == "shift":
        shift_mod: int = 1
    if shift_type == "inv_shift":
        shift_mod: int = -1

    # First row: no shift
    rows[1] = rows[1][shift_mod * 1:] + rows[1][:1 * shift_mod]
    rows[2] = rows[2][shift_mod * 2:] + rows[2][:2 * shift_mod]
    rows[3] = rows[3][shift_mod * 3:] + rows[3][:3 * shift_mod]

    if type(rows[0][0]) == bytes:
        rows = [[ord(byte) for byte in row] for row in rows]
        block_shifted: bytes = bytes(sum(rows, []))
    else:
        block_shifted: bytes = bytes(sum(rows, []))

    return block_shifted

