import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from working_with_a_file import read_bytes, write_bytes_text, write_file


class Symmetric:
    """
    A class that implements symmetric encryption using the SM4 algorithm.

    Attributes
        key: encryption key
    """
    def __init__(self):
        self.key = None

    def generate_key(self) -> bytes:
        """
        Generates a random 16 byte encryption key.

        Returns
            The generated encryption key.
        """
        self.key = os.urandom(16)
        return self.key

    def key_deserialization(self, file_name: str) -> None:
        """
        Deserializes the encryption key from a file.

        Parameters
            file_name: The path to the file containing the encryption key.
        """
        try:
            with open(file_name, "rb") as file:
                self.key = file.read()
        except FileNotFoundError:
            print("The file was not found")
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}")

    def serialize_sym_key(self, path: str) -> None:
        """
        Serializes the encryption key to a file.

        Parameters
            path: The path to the file where the encryption key will be saved.
        """
        try:
            with open(path, 'wb') as key_file:
                key_file.write(self.key)
        except FileNotFoundError:
            print("The file was not found")
        except Exception as e:
            print(f"An error occurred while writing the file: {str(e)}")

    def encrypt(self, path_text: str, encrypted_path_text: str) -> bytes:
        """
        Encrypts data from a file using the SM4 algorithm in CFB mode.

        Parameters
            path_text: The path to the file with the source data.
            encrypted_path_text: The path to the file where the encrypted data will be written.
        Returns
            The encrypted data.
        """
        text = read_bytes(path_text)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.SM4(self.key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        padder = padding.ANSIX923(32).padder()
        padded_text = padder.update(text) + padder.finalize()
        cipher_text = iv + encryptor.update(padded_text) + encryptor.finalize()
        write_bytes_text(encrypted_path_text, cipher_text)
        return cipher_text

    def decrypt(self, encrypted_path_text: str, decrypted_path_text: str) -> str:
        """
        Decrypts data from a file using the SM4 algorithm in CFB mode.

        Parameters
            encrypted_path_text: The path to the file with the encrypted data.
            decrypted_path_text: The path to the file where the decrypted data will be written.
        Returns
            The decrypted data as a string.
        """
        encrypted_text = read_bytes(encrypted_path_text)
        iv = encrypted_text[:16]
        cipher_text = encrypted_text[16:]
        cipher = Cipher(algorithms.SM4(self.key), modes.CFB(iv))
        decryptor = cipher.decryptor()
        d_text = decryptor.update(cipher_text) + decryptor.finalize()
        unpadder = padding.ANSIX923(128).unpadder()
        unpadded_dc_text = unpadder.update(d_text) + unpadder.finalize()
        d_text = unpadded_dc_text.decode('UTF-8')
        write_file(decrypted_path_text, d_text)
        return d_text
