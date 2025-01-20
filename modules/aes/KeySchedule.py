from modules import DataPreparation, cbcOperations
from modules.aes import SubBytes


def key_schedule(cipher_key: bytes, key_size: int) -> list[bytes]:
    # Determining parameters based on the key size
    # cipher_key_words_length => number of words in the initial key based on the key size / AES mode
    # total_words => total number of words required for all the round keys
    # rcon_mod => usage of rcon every x words (also used to calculate the index of the rcon value to use during XOR)
    if key_size == 16:
        cipher_key_words_length: int = 4
        total_words: int = 44  # 10 round keys
        rcon_mod: int = 4

    if key_size == 24:
        cipher_key_words_length: int = 6
        total_words: int = 58  # 13 round keys
        rcon_mod: int = 6

    if key_size == 32:
        cipher_key_words_length: int = 8
        total_words: int = 68  # 15 round keys
        rcon_mod: int = 8

    # Splitting the key into 4 words of 4 bytes each
    words_list: list[bytes] = DataPreparation.divide_into_blocks(cipher_key, 4)

    # Generating round keys for AES-128 and AES-256
    if key_size == 16 or key_size == 32:
        for word_index in range(cipher_key_words_length, total_words):
            if word_index % 4 == 0:
                gen_round_key_first_word(word_index, words_list, rcon_mod)
            else:
                gen_round_key_other_words(word_index, words_list, rcon_mod)

    # Generating round keys for AES-192
    if key_size == 24:
        for word_index in range(cipher_key_words_length, total_words):
            # With an initial 6-word key, we subtract 2 to get multiples of 4
            if (word_index - 2) % 4 == 0:
                gen_round_key_first_word(word_index, words_list, rcon_mod)
            else:
                gen_round_key_other_words(word_index, words_list, rcon_mod)

    round_keys: list[bytes] = format_words_list(words_list, cipher_key_words_length)
    return round_keys


def gen_round_key_first_word(word_index: int, words_list: list[bytes], rcon_mod: int) -> list[bytes]:
    # Retrieve the index from the RCON list to use based on the current word index
    rcon_indicie: int = (word_index // rcon_mod) - 1
    round_key_first_word: bytes = DataPreparation.rot_word(words_list[word_index - 1])
    round_key_first_word = SubBytes.subbytes_operations(round_key_first_word, "s_box")
    round_key_first_word = cbcOperations.xor(round_key_first_word, words_list[word_index - 4], 4)

    # Performs XOR with RCON every 4, 6, or 8 words
    if word_index % rcon_mod == 0:
        round_key_first_word = cbcOperations.xor(round_key_first_word, rcon[rcon_indicie], 4)

    words_list.append(round_key_first_word)
    return words_list


def gen_round_key_other_words(word_index: int, words_list: list[bytes], rcon_mod: int) -> list[bytes]:
    # Retrieve the index from the RCON list to use based on the current word index
    rcon_indicie: int = (word_index // rcon_mod) - 1
    round_key_other_byte: bytes = cbcOperations.xor(words_list[word_index - 1], words_list[word_index - 4], 4)

    # Performs XOR with RCON every 4, 6, or 8 words
    if word_index % rcon_mod == 0:
        round_key_other_byte = cbcOperations.xor(round_key_other_byte, rcon[rcon_indicie], 4)

    words_list.append(round_key_other_byte)
    return words_list


def format_words_list(words_list: list[bytes], cipher_key_words_length: int) -> list[bytes]:
    round_keys: list[bytes] = []
    for i in range(cipher_key_words_length, len(words_list), 4):
        round_key: bytes = b''.join(words_list[i:i + 4])
        round_keys.append(round_key)
    return round_keys


rcon = [
    [0x01, 0x00, 0x00, 0x00],
    [0x02, 0x00, 0x00, 0x00],
    [0x04, 0x00, 0x00, 0x00],
    [0x08, 0x00, 0x00, 0x00],
    [0x10, 0x00, 0x00, 0x00],
    [0x20, 0x00, 0x00, 0x00],
    [0x40, 0x00, 0x00, 0x00],
    [0x80, 0x00, 0x00, 0x00],
    [0x1b, 0x00, 0x00, 0x00],
    [0x36, 0x00, 0x00, 0x00]
]
