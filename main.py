import argparse
import time
from modules import EncryptDecryptProcess


def main() -> None:
    """
    Main function that encrypts or decrypts a file using AES in CBC mode.
    The operation mode (encryption or decryption) and the files to process are specified via command-line arguments.

    Command-line parameters:
        -m, --mode : execution mode, 'encrypt' to encrypt or 'decrypt' to decrypt a file
        -i, --input : path to the file to be processed (to encrypt or decrypt)
        -o, --output : path where the encrypted or decrypted file will be saved
        -k, --key : path to the file containing the decryption key (only for 'decrypt')
        -s, --size : size of the AES key in bits (128 by default, 192 or 256), only for 'encrypt'
    """

    parser = argparse.ArgumentParser(description="Encrypt / Decrypt a file with AES algorithm in CBC mode")
    parser.add_argument("-m", "--mode", type=str, choices=["encrypt", "decrypt"], required=True,
        help="Execution mode: 'encrypt' to encrypt, 'decrypt' to decrypt a file")
    parser.add_argument("-i", "--input", type=str, required=True,
        help="Path to the file to be processed (to encrypt or decrypt depending on the selected mode)")
    parser.add_argument("-o", "--output", type=str, required=True,
        help="Path where the encrypted or decrypted file will be saved")
    parser.add_argument("-k", "--key", type=str, required=False,
        help="Path to the file containing the decryption key (necessary only in 'decrypt' mode)")
    parser.add_argument("-s", "--size", type=int, choices=[128, 192, 256], default=128, required=False,
        help="Size of the key used by AES in bits (128 by default, 192, 256, used only in 'encrypt' mode)")

    args = parser.parse_args()
    mode: str = args.mode
    input_file_path: str = args.input
    output_file_path: str = args.output
    key_file_path: str = args.key
    key_size: int = (args.size)//8

    block_size: int = 16
    start_time: float = time.perf_counter()

    if mode == "encrypt":
        EncryptDecryptProcess.encrypt_file(input_file_path, output_file_path, key_size, block_size)
    elif mode == "decrypt":
        EncryptDecryptProcess.decrypt_file(input_file_path, output_file_path, key_file_path)

    end_time: float = time.perf_counter()
    execution_time: float = (end_time - start_time) * 1000000
    print(f"Execution time : {round(execution_time, 6)} microseconds")
    print("Done !")


if __name__ == "__main__":
    main()