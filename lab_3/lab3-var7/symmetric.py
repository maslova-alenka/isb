import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from working_with_a_file import read_bytes, write_bytes_text, write_file, deserialization_sym_key


class Symmetric:
    def __init__(self):
        self.key = None

    def generate_key(self) -> bytes:
        self.key = os.urandom(16)
        return self.key

    def key_deserialization(self, file_name: str) -> None:
        with open(file_name, "rb") as file:
            self.key = file.read()

    def encrypt(self, path_text, encrypted_path_text):
        text = read_bytes(path_text)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.SM4(self.key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        padder = padding.ANSIX923(32).padder()
        padded_text = padder.update(text) + padder.finalize()
        cipher_text = iv + encryptor.update(padded_text) + encryptor.finalize()
        write_bytes_text(encrypted_path_text, cipher_text)
        return iv + cipher_text

    def decrypt(self, path_key, encrypted_path_text, decrypted_path_text):
        encrypted_text = read_bytes(encrypted_path_text)
        iv = encrypted_text[:16]
        cipher_text = encrypted_text[16:]
        self.key = deserialization_sym_key(path_key)
        cipher = Cipher(algorithms.SM4(self.key), modes.CFB(iv))
        decryptor = cipher.decryptor()
        d_text = decryptor.update(cipher_text) + decryptor.finalize()
        unpadder = padding.ANSIX923(128).unpadder()
        unpadded_dc_text = unpadder.update(d_text) + unpadder.finalize()
        d_text = unpadded_dc_text.decode('UTF-8')
        write_file(decrypted_path_text, d_text)
        return d_text

    def serialize_sym_key(self, path: str) -> None:
        with open(path, 'wb') as key_file:
            key_file.write(self.key)
