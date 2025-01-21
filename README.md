# PyCBC_AES

A pure Python implementation of AES encryption and decryption in CBC mode, without relying on external libraries. This tool can encrypt and decrypt any type of file.

## Features

- **AES-CBC Encryption/Decryption:** Implements AES in Cipher Block Chaining (CBC) mode from scratch.
- **File Support:** Handles encryption and decryption of any file type (e.g., text, images, videos ...).
- **Pure Python:** No external libraries required for cryptographic operations.
- **Key Size Options:** Supports AES key sizes of 128, 192, and 256 bits.
- **Secure:** Includes IV-based chaining for enhanced security.

## Requierements

- Python 3.10 or higher
- No additional dependencies

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/py_cbc_aes.git
   ```
    
2. Navigate to the project directory:
   ```bash
   cd py_cbc_aes
   ```

3. Ensure Python 3.10+ is installed:
   ```bash
   python --version
   ```

## Usage
   
### Command-line Arguments  

- `-m` / `--mode`: Specify the mode of operation:  
  - `encrypt`: To encrypt a file.  
  - `decrypt`: To decrypt a file.  

- `-i` / `--input`: Path to the input file (the file to encrypt or decrypt).  

- `-o` / `--output`: Path where the processed file will be saved.  

- `-k` / `--key`: Path to the key file (required for decryption).  

- `-s` / `--size`: AES key size in bits (only for encryption).  
  - Valid values: `128`, `192`, or `256`.  
  - Default: `128`.

### Examples  

#### Encrypting a File  

```bash
python main.py -m encrypt -i example.txt -o example.enc -s 256
```
This command will:
- Encrypt the file example.txt using a 256-bit AES key.
- Save the encrypted file as example.enc.
- Save the key used in the encryption process as example_key.bin.

#### Decrypting a File
```bash
python main.py -m decrypt -i example.enc -o example_dec.txt -k example_key.bin
```
This command will:
- Decrypt the file example.enc using the key stored in example_key.bin.
- Save the decrypted content to example_dec.txt.

#### Notes
During encryption, the program automatically generates a key file.
This key file will have the same name as the input file with the suffix _key.
For example, if the input file is file.txt, the generated key file will be named file_key.bin.

## License

This program is free software: you are allowed to redistribute and/or modify it under the terms of the **GNU General Public License** (GPL), as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed with the expectation that it will be useful, but **without any warranty**. For more information, see the **GPL**.

You should have received a copy of the **GPL** along with this program. If not, visit [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
